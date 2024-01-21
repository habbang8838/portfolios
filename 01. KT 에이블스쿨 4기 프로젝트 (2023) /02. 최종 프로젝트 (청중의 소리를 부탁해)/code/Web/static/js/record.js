const startButton = document.querySelector("#record-button");
const stopButton = document.querySelector("#stop-button");
const videoElement = document.querySelector("#preview");
const navigationButtons = document.querySelectorAll("#nav-btn");
const currentLectureId = document.getElementById("id").dataset.id;
const elapsedTimeDisplay = document.getElementById('elapsed-time');
const recordingInterval = parseInt(document.getElementById("term").dataset.term);

let recorder;
let recordedVideoChunks;
let recordingIntervalId;
let elapsedTimeUpdateIntervalId;
let recordingStartTime;
let recordingElapsedTime;
let isSaved = false;
let isRecording = false;
let isRecordingStopped = false;
let pendingUploadsCount = 0;


function initiateRecording() {
    console.log('Initiate video recording');
    navigator.mediaDevices.getUserMedia({video: true, audio: true}).then(stream => {
        videoElement.srcObject = stream;
        startRecording(videoElement.captureStream())
    })

    isRecording = true;
    recordingStartTime = Date.now();
    recordingElapsedTime = 0;

    elapsedTimeUpdateIntervalId = setInterval(displayElapsedTime, 1000);
    recordingIntervalId = setInterval(handleRecordingInterval, 60000 * recordingInterval);
}


function startRecording(stream) {
    recordedVideoChunks = [];
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => {
        recordedVideoChunks.push(e.data)
    }

    recorder.start();
}

function displayElapsedTime() {
    const elapsedTime = Date.now() - recordingStartTime;
    const hours = formatElapsedTime(elapsedTime / 3600000);
    const minutes = formatElapsedTime((elapsedTime % 3600000) / 60000);
    const seconds = formatElapsedTime((elapsedTime % 60000) / 1000);

    elapsedTimeDisplay.textContent = `${hours}:${minutes}:${seconds}`;
}

function formatElapsedTime(time) {
    return Math.floor(time).toString().padStart(2, '0')
}

function handleRecordingInterval() {
    if (!recorder) {
        return;
    }

    if (recorder.state === "recording") {
        recorder.stop();
        recorder.onstop = processRecordedMedia;
    }

    if (recorder.state === "inactive") {
        recorder.start();
        recordingElapsedTime += recordingInterval;
    }
}

async function processRecordedMedia() {
    const video = new Blob(recordedVideoChunks, {type: "video/webm"});

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async (image) => {
        try {
            await uploadRecordedMedia(image, video);
        } catch (error) {
            console.error(error);
        }
    }, 'image/png');

    recordedVideoChunks = [];
}


function uploadRecordedMedia(image, video) {
    const formData = new FormData();
    formData.append('lecture_id', currentLectureId);
    formData.append('time', recordingElapsedTime);
    formData.append('image', image);
    formData.append('video', video);

    pendingUploadsCount += 1;

    $.ajax({
        url: '/live/video/',
        data: formData,
        method: 'POST',
        processData: false,
        contentType: false,
        success: function (result) {
            console.log('Upload recorded media');

            pendingUploadsCount -= 1;
            completeRecordingSession();

            const data = $.parseJSON(result);
            if ($.isEmptyObject(data)) {
                console.log('얼굴 인식 실패');
                return;
            }

            const emotion = $('#emotionImage');
            $('#reaction').empty();
            let audience_reaction = data['concentration'];
            $('#concentrationTextElement').text("집중도: " + audience_reaction + "%");
            if (audience_reaction >= 70) {
                console.log('긍정')
                emotion.attr("src", "/static/img/emotion/smile.png");
            } else if (audience_reaction >= 40) {
                console.log('중립')
                emotion.attr("src", "/static/img/emotion/neutral.png");
            } else {
                console.log('부정')
                emotion.attr("src", "/static/img/emotion/bad.png");
            }

            isSaved = true;
        },
        error: function (request, status, error) {
            console.log('에러');
            console.log('code:' + request.status + '\n' + 'message:' + request.responseText + '\n' + 'error:' + error);
            console.log(request);
            console.log(status);
            console.log(error);
        }
    })
}

function stopRecording() {
    if (!confirmStopRecording()) {
        return;
    }

    console.log("Stop recording");
    recorder.stop();
    videoElement.srcObject.getTracks().forEach(track => track.stop());

    clearInterval(recordingIntervalId);
    clearInterval(elapsedTimeUpdateIntervalId);

    if (!isSaved) {
        deleteLecture()
        return;
    }

    isRecordingStopped = true;
    submitLectureTimes(Date.now());
}

function confirmStopRecording() {
    if (isRecording && !isSaved) {
        return confirm("분석된 결과가 없습니다. 중단하시겠습니까?");
    }

    if (isRecording && !isRecordingStopped) {
        return confirm("현재 반응 분석이 진행 중입니다. 중단하시겠습니까?");
    }

    return false;
}

function deleteLecture() {
    const formData = new FormData();
    formData.append('lecture_id', currentLectureId);

    $.ajax({
        url: '/report/list/delete/',
        data: formData,
        method: 'POST',
        processData: false,
        contentType: false,
        success: function (result) {
            console.log('성공')
            location.replace('/report/list');
        },
        error: function (result, status, error) {
            console.log('에러')
            console.log(result);
            console.log(status);
            console.log(error);
        }
    })
}

function submitLectureTimes(recordingEndTime) {
    const formData = new FormData();
    formData.append('lecture_id', currentLectureId);
    formData.append('start_time', toTimeString(recordingStartTime));
    formData.append('end_time', toTimeString(recordingEndTime));

    $.ajax({
        url: '/live/time/',
        data: formData,
        method: 'POST',
        processData: false,
        contentType: false,
        success: function (result) {
            console.log('Submit lecture times');
            $('#loading').show();
            $('body').css('overflow', 'hidden');
        },
        error: function (request, status, error) {
            console.log('에러');
            console.log(request);
            console.log(status);
            console.log(error);
        },
        complete: function () {
            console.log('완료');
            completeRecordingSession();
        }
    })
}

function toTimeString(timestamp) {
    return new Date(timestamp).toISOString().split('T')[1].split('.')[0];
}

function completeRecordingSession() {
    if (isRecordingStopped && (pendingUploadsCount === 0)) {
        setTimeout(function () {
            $('body').css('overflow', 'auto');
            location.href = '/report/result/' + currentLectureId + '/';
        }, 5000);
    }
}

startButton.addEventListener("click", initiateRecording);
stopButton.addEventListener("click", stopRecording);
navigationButtons.forEach((button) => {
    button.addEventListener('click', stopRecording)
});