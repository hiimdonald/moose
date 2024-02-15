let gameTimeRemaining;
let gameActive = false;
let timerInterval;

function setTimer(minutes) {
  gameTimeRemaining = minutes * 60; // Convert minutes to seconds
  gameActive = true;
  updateTimerDisplay();
  startTimer();
}

function startTimer() {
  clearInterval(timerInterval); // Clear any existing timer intervals
  timerInterval = setInterval(function () {
    gameTimeRemaining--;
    updateTimerDisplay();

    if (gameTimeRemaining <= 0) {
      clearInterval(timerInterval);
      gameActive = false;
      alert(
        "Time's up! You answered " +
          numCorrect +
          "out of " +
          (numWrong + numWrong) +
          "correct! Your score: " +
          score +
          "%"
      );
    }
  }, 1000); // Update every second
}

function updateTimerDisplay() {
  const minutes = Math.floor(gameTimeRemaining / 60);
  const seconds = gameTimeRemaining % 60;
  document.getElementById("timerDisplay").textContent = `${minutes}:${
    seconds < 10 ? "0" : ""
  }${seconds}`;
}

function stopTimer() {
  clearInterval(timerInterval); // Stop the timer
  gameActive = false; // Set game as inactive
  document.getElementById("timerDisplay").textContent = "Timer stopped";
}
