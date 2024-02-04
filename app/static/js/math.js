const options = document.querySelectorAll(".options");
let currentDifficulty = "easy"; // Default difficulty
let currentOperation = "addition"; // Default operation
let numCorrect = 0,
  numWrong = 0,
  score = 0;
let selectedOption = null; // Keep track of the selected option

// Event listener for each option
options.forEach((option) => {
  option.addEventListener("click", function () {
    // Remove 'option-selected' class from all options
    options.forEach((opt) => opt.classList.remove("option-selected"));
    // Add 'option-selected' class to the clicked option
    this.classList.add("option-selected");
    selectedOption = this; // Update the selected option
  });
});

// Submit button event listener
document.getElementById("submit-answer").addEventListener("click", function () {
  if (!selectedOption) {
    alert("Please select an answer before submitting.");
  } else {
    checkAnswer(selectedOption);
    // Reset selectedOption after submission
    selectedOption.classList.remove("option-selected");
    selectedOption = null;
  }
});

function startGame(difficulty, operation) {
  currentDifficulty = difficulty;
  currentOperation = operation;
  fetchEquation();
}

function fetchEquation() {
  const url = `/api/mock_generate_numbers?difficulty=${currentDifficulty}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const correctAnswer =
        currentOperation === "subtraction"
          ? data.number1 - data.number2
          : data.number1 + data.number2;
      displayEquation(data.number1, data.number2);
      prepareOptions(correctAnswer);
    })
    .catch((error) => console.error("Error fetching equation:", error));
}

function displayEquation(num1, num2) {
  document.getElementById("num1").textContent = num1;
  document.getElementById("num2").textContent = num2;
  document.querySelector(".operator").textContent =
    currentOperation === "subtraction" ? "-" : "+";
}

function prepareOptions(correctAnswer) {
  let answers = generateOptions(correctAnswer);
  answers.forEach((answer, index) => {
    options[index].textContent = answer.value;
    options[index].dataset.correct = answer.isCorrect;
    // Remove previous styles
    options[index].classList.remove("correct", "incorrect", "option-selected");
  });
}

// function generateOptions(correctAnswer) {
//   let answers = [correctAnswer];
//   while (answers.length < 3) {
//     let option = correctAnswer + Math.floor(Math.random() * 10) - 5;
//     if (!answers.includes(option)) answers.push(option);
//   }
//   return answers.map((value) => ({
//     value,
//     isCorrect: value === correctAnswer,
//   }));
// }

function generateOptions(correctAnswer) {
  let options = [{ value: correctAnswer, isCorrect: true }];

  // Generate two more unique incorrect options
  while (options.length < 3) {
    let incorrectOption = correctAnswer + Math.floor(Math.random() * 10) - 5;

    // Ensure the incorrect option is positive
    incorrectOption = Math.abs(incorrectOption);

    // Check for uniqueness
    let isUnique = !options.some((option) => option.value === incorrectOption);

    if (isUnique) {
      options.push({ value: incorrectOption, isCorrect: false });
    }
  }

  // Shuffle options
  return options.sort(() => Math.random() - 0.5);
}

function checkAnswer(option) {
  const isCorrect = option.dataset.correct === "true";
  // Update score based on the selected answer
  updateScore(isCorrect);

  // Show feedback and wait before loading new question
  showFeedback(isCorrect);

  // Ensure the feedback is visible for a short period before moving to the next question
  setTimeout(() => {
    // Reset the display for a new question
    resetDisplayForNewQuestion();
    // Fetch a new equation after feedback has been shown
    fetchEquation();
  }, 1000); // Delay for new problem
}

function showFeedback(isCorrect) {
  const equationElement = document.querySelector(".equation");
  equationElement.innerHTML = isCorrect
    ? '<h1 style="color: green;">Correct!</h1>'
    : '<h1 style="color: red;">Wrong!</h1>';
}

function updateScore(isCorrect) {
  if (isCorrect) numCorrect++;
  else numWrong++;
  document.getElementById("correct-count").textContent = numCorrect;
  document.getElementById("incorrect-count").textContent = numWrong;
  let total = numCorrect + numWrong;
  score = total > 0 ? Math.round((numCorrect / total) * 100) : 0;
  document.getElementById("score").textContent = score + "%";
}

function resetDisplayForNewQuestion() {
  // Reset the equation display to its original format
  const equationElement = document.querySelector(".equation");
  equationElement.innerHTML = `
      <h1 id="num1" style="color: #6181f8"></h1>
      <span class="operator" style="color: #2ab7ca">+</span> <!-- Default operator -->
      <h1 id="num2" style="color: #fed766"></h1>
      <h1 style="color: #f86624">=</h1>
      <h1 id="result" style="color: gray">?</h1>
  `;

  // Clear any selection from options
  options.forEach((option) =>
    option.classList.remove("option-selected", "correct", "incorrect")
  );

  // Reset selectedOption for the next question
  selectedOption = null;
}

// Initially start the game
startGame(currentDifficulty, currentOperation);
