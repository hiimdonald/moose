document.addEventListener("DOMContentLoaded", (event) => {
  fetchNextProblem("easy"); // Default to 'easy' for testing
});

function checkAnswer(selectedOption) {
  const isCorrect = selectedOption.getAttribute("data-answer") === "true";
  updateScore(isCorrect);
  // Fetch the next problem with the same difficulty as the current one
  const currentDifficulty = "easy"; // This should be dynamic based on the user's selection
  fetchNextProblem(currentDifficulty);
}

function updateScore(isCorrect) {
  const correctCountEl = document.getElementById("correct-count");
  const incorrectCountEl = document.getElementById("incorrect-count");
  const scoreEl = document.getElementById("score");

  let correctCount = parseInt(correctCountEl.textContent, 10);
  let incorrectCount = parseInt(incorrectCountEl.textContent, 10);

  if (isCorrect) {
    correctCount++;
  } else {
    incorrectCount++;
  }

  correctCountEl.textContent = correctCount;
  incorrectCountEl.textContent = incorrectCount;

  // Update the score; you might define score differently
  scoreEl.textContent = correctCount - incorrectCount;
}

function fetchNextProblem(difficulty) {
  fetch(`/get_math_problem?difficulty=${difficulty}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("num1").textContent = data.number1;
      document.getElementById("num2").textContent = data.number2;

      // Reset previous options
      const options = document.querySelectorAll(".options");
      options.forEach((option, index) => {
        // Assuming data.options is an array of {value, isCorrect}
        if (data.options && index < data.options.length) {
          option.children[0].textContent = data.options[index].value; // Update the <h1> within .options div
          option.setAttribute("data-answer", data.options[index].isCorrect); // Update data-answer attribute
          option.style.display = "block"; // Make sure the option is visible
        } else {
          option.style.display = "none"; // Hide extra options if any
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching the next problem:", error);
    });
}

function startGame(difficulty) {
  fetchNextProblem(difficulty);
}
