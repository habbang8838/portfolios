import json
import os
import os.path
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from monitoring.settings import MEDIA_ROOT
from report.models import Feedback, Reaction
from .models import Lecture
from .utils import analyze_image, extract_audio, upload_to_storage, save_blob, clean_up_files, run_stt, \
    generate_feedback

BUCKET_NAME = 'stt-test-bucket-aivle'


@csrf_exempt
@login_required
def info(request):
    if request.method == "GET":
        return render(request, "live/lecture_preset.html")

    if request.method == "POST":
        topic = request.POST.get("topic")
        term = request.POST.get("term")
        category = request.POST.get("category")

        if not all([topic, term, category]):
            return JsonResponse({'error': 'Missing data'}, status=400)

        user = request.user
        lecture = Lecture(topic=topic, category=category, user=user)
        lecture.save()

        request.session["lecture_id"] = lecture.id

        return redirect("live:record", id=lecture.id, term=term)


@csrf_exempt
@login_required
def record(request, id, term):
    session_lecture_id = request.session.get("lecture_id")
    if not session_lecture_id or session_lecture_id != id:
        return redirect("live:info")

    if request.method == "GET":
        lecture = get_object_or_404(Lecture, id=id)
        context = {'id': id, 'term': term, 'topic': lecture.topic}
        return render(request, "live/analysis_page.html", context)


@csrf_exempt
def process_media(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        image = request.FILES['image']
        video = request.FILES['video']
    except KeyError:
        return JsonResponse({'error': 'Missing files'}, status=400)

    lecture_id = request.POST.get('lecture_id')
    lecture_time = request.POST.get('time')

    if not lecture_id or not lecture_time:
        return JsonResponse({'error': 'Missing data'}, status=400)

    uuid_name = uuid4().hex
    image_path = os.path.join(MEDIA_ROOT, f"{uuid_name}.jpg")
    save_blob(image, image_path)

    results = analyze_image(image_path)  # haarcascade 모델

    if not results or sum(results.values()) == 0:
        clean_up_files([image_path])
        return HttpResponse(json.dumps({}))

    lecture = get_object_or_404(Lecture, pk=lecture_id)

    reaction = Reaction(
        lecture=lecture,
        time=lecture_time,
        concentration=results.get("concentration", 0),
        negative=results.get("negative", 0),
        neutral=results.get("neutral", 0),
        positive=results.get("positive", 0)
    )
    reaction.save()

    video_path = os.path.join(MEDIA_ROOT, f"{uuid_name}.mp4")
    save_blob(video, video_path)

    audio_path = extract_audio(video_path)
    upload_file_name = f"{uuid_name}.mp3"
    upload_to_storage(BUCKET_NAME, audio_path, upload_file_name)

    audio_content = run_stt(BUCKET_NAME, upload_file_name)

    feedback_content = generate_feedback(lecture.topic, lecture.category, audio_content, reaction)
    feedback = Feedback(
        reaction=reaction,
        content=feedback_content
    )
    feedback.save()

    clean_up_files([image_path, video_path, audio_path])

    return HttpResponse(json.dumps(results))


@csrf_exempt
def update_lecture_time(request):
    if request.method == "POST":
        lecture_id = request.POST.get("lecture_id")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        if not all([lecture_id, start_time, end_time]):
            return JsonResponse({'error': 'Missing data'}, status=400)

        try:
            lecture = get_object_or_404(Lecture, pk=lecture_id)
            reactions = Reaction.objects.filter(lecture=lecture)

            if reactions.exists():
                lecture.start_time = start_time
                lecture.end_time = end_time
                lecture.save()
                print("'message': 'Lecture times updated successfully'")
                return JsonResponse({'message': 'Lecture times updated successfully'}, status=200)
            else:
                lecture.delete()
                print("'message': 'Lecture deleted successfully'")
                return JsonResponse({'message': 'Lecture deleted successfully'}, status=200)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
