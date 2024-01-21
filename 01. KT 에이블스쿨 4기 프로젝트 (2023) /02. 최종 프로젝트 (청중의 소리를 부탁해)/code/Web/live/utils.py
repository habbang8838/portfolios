import os
import os.path

import cv2
import moviepy.editor as mp
import numpy as np
from django.core.files.storage import default_storage
from google.cloud import speech
from google.cloud import storage
from google.oauth2 import service_account
from openai import OpenAI
from tensorflow.keras.models import load_model

from monitoring import settings

KEY_PATH = settings.STT_API_KEY
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

client = storage.Client(credentials=credentials, project=credentials.project_id)

openai = OpenAI(api_key=settings.GPT_API_KEY)


def save_blob(file, path):
    with default_storage.open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def clean_up_files(paths):
    for path in paths:
        try:
            os.remove(path)
        except OSError as e:
            print(f"Error deleting file {path}: {e.strerror}")


def extract_audio(video_path):
    audio_path = video_path.split(".mp4")[0] + ".mp3"
    mp.ffmpeg_tools.ffmpeg_extract_audio(video_path, audio_path)

    return audio_path


def upload_to_storage(bucket_name, source_file_path, destination_blob_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    return blob.public_url


def run_stt(bucket_name, upload_file_name):
    client = speech.SpeechClient()

    gcs_uri = f"gs://{bucket_name}/{upload_file_name}"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        audio_channel_count=1,
        language_code="ko-KR",
    )

    res = client.long_running_recognize(config=config, audio=audio)
    response = res.result()

    audio_content = ""
    for result in response.results:
        audio_content += result.alternatives[0].transcript

    return audio_content


def generate_feedback(topic, category, prompt, reaction):
    content = (
        f"주제: {topic}\n"
        f"카테고리: {category}\n"
        f"청중 반응: 집중도 {reaction.concentration}%, 긍정 {reaction.positive}%, "
        f"중립 {reaction.neutral}%, 부정 {reaction.negative}%\n"
        f"내용: {prompt}"
    )
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "당신은 교육 전문가로서, 강의 내용에 대한 피드백을 "
                           "제공해야 합니다. 강점, 약점, 개선 방법을 순서대로 작성해주세요."
                           "발음이나 억양, 속도 등의 음성적 특성에 대한 피드백은 제외하고, "
                           "오로지 강의 내용과 청중의 반응에 초점을 맞춰주세요.\n"
                           "[피드백 형식]\n"
                           "강점:\n- [강점을 기재해 주세요]\n"
                           "약점:\n- [약점을 기재해 주세요]\n"
                           "개선 방법:\n- [개선 방법을 기재해 주세요]",
            },
            {"role": "user", "content": content},
        ],
    )

    result = completion.choices[0].message.content

    return result


def analyze_image(image_path):
    def load_detection_model(model_path):
        detection_model = cv2.CascadeClassifier(model_path)
        return detection_model

    def detect_faces(detection_model, gray_image_array):
        return detection_model.detectMultiScale(gray_image_array, 1.3, 5)

    def draw_bounding_box(face_coordinates, image_array, color):
        x, y, w, h = face_coordinates
        cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)

    def apply_offsets(face_coordinates, offsets):
        x, y, width, height = face_coordinates
        x_off, y_off = offsets
        return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)

    def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0, font_scale=0.5, thickness=2):
        x, y = coordinates[:2]
        cv2.putText(image_array, text, (x + x_offset, y + y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color,
                    thickness, cv2.LINE_AA)

    def preprocess_input(x, v2=True):
        x = x.astype('float32')
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x

    image_path = image_path
    detection_model_path = 'haarcascade_frontalface_default.xml'

    emotion_model_path = 'selfCNN2.h5'
    emotion_labels = {0: 'angry', 1: 'fear', 2: 'happy', 3: 'sad', 4: 'surprise', 5: 'neutral'}
    font = cv2.FONT_HERSHEY_SIMPLEX

    emotion_offsets = (0, 0)

    # model load
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    emotion_target_size = emotion_classifier.input_shape[1:3]

    rgb_image = cv2.imread(image_path)
    gray_image = cv2.imread(image_path, 0)

    def highest_emotion(positive, neutral, negative):
        if positive == max([positive, neutral, negative]):
            return 'positive'
        elif neutral == max([positive, neutral, negative]):
            return 'neutral'
        else:
            return 'negative'

    def engagement_score(scores):
        if ((scores[5] > 0.6) | (scores[2] > 0.5) | (scores[4] > 0.6) | (scores[0] > 0.2) | (scores[1] > 0.3) | (
                scores[3] > 0.3)):
            return ((scores[0] * 0.25) + (scores[1] * 0.3) + (scores[2] * 0.6) + (scores[3] * 0.3) + (
                    scores[4] * 0.6) + (scores[5] * 0.9))
        else:
            return 0

    positives = []
    neutrals = []
    negatives = []
    engagements = []
    faces = detect_faces(face_detection, rgb_image)
    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        gray_face = cv2.resize(gray_face, (emotion_target_size))

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)

        emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
        engagement = engagement_score(emotion_classifier.predict(gray_face)[0])
        positive = emotion_classifier.predict(gray_face)[0][2] + emotion_classifier.predict(gray_face)[0][4]
        neutral = emotion_classifier.predict(gray_face)[0][5]
        negative = emotion_classifier.predict(gray_face)[0][0] + emotion_classifier.predict(gray_face)[0][1] + \
                   emotion_classifier.predict(gray_face)[0][3]
        positives.append(positive)
        neutrals.append(neutral)
        negatives.append(negative)
        engagements.append(engagement)
        emotion_text = highest_emotion(positive, neutral, negative)
        color = (0, 255, 255)

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_text, color, -20, -20, 0.7, 2)

    # plt.imshow(rgb_image)
    # cv2.imwrite('result_emotion_image.jpg', rgb_image)

    def calculate_percentage(emotion):
        if len(emotion) == 0:
            return 0
        else:
            return int(round(sum(emotion) / len(emotion), 2) * 100)

    positive = calculate_percentage(positives)
    neutral = calculate_percentage(neutrals)
    negative = calculate_percentage(negatives)
    concentration = calculate_percentage(engagements)
    results = {
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "concentration": concentration,
    }

    return results
