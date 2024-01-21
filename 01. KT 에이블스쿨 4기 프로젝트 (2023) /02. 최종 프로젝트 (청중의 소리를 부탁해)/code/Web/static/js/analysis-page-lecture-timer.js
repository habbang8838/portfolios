let startTime;
let updatedTime;
let difference;
let tInterval;
let running = false;
let timerDisplay = document.getElementById('timer');
let startButton = document.getElementById('LectureStart');
let stopButton = document.getElementById('LectureStop');

function startTimer(){
  if(!running){
    startTime = new Date().getTime();
    tInterval = setInterval(getShowTime, 1000);
    running = true;
    startButton.disabled = true;
    stopButton.disabled = false;
  }
}

function stopTimer(){
  clearInterval(tInterval);
  running = false;
  startButton.disabled = false;
  stopButton.disabled = true;
}

function getShowTime(){
  updatedTime = new Date().getTime();
  difference = updatedTime - startTime;
  let hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  let minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
  let seconds = Math.floor((difference % (1000 * 60)) / 1000);

  hours = (hours < 10) ? "0" + hours : hours;
  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;

  timerDisplay.innerHTML = hours + ':' + minutes + ':' + seconds;
}

startButton.addEventListener('click', startTimer);
stopButton.addEventListener('click', stopTimer);
