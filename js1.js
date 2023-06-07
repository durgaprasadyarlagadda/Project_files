
const quizData = [
    {
        question: "How is an array initialized in C language?",
        options: ["int a[3] = {1,2,3};", "int a = {1,2,3};", "int a[] = new int[3];", "int a(3) = [1,2,3];"],
        answer: 0
    },
    {
        question: "If p is an integer pointer with a value 1000, then what will the value of p + 5 be?",
        options: ["1005", "1020", "1010", "1015"],
        answer: 1
    },
    {
        question: "Which of the following are not standard header files in C?",
        options: ["stdio.h", "stdlib.h", "math.h", "None of the above"],
        answer: 3
    },
    {
        question: "In which of the following languages is function overloading not possible?",
        options: ["C", "C++", "Python", "Java"],
        answer: 0
    },
    {
        question: "Which data structure is used to handle recursion in C?",
        options: ["Stack", "Queue", "Deque", "Trees"],
        answer: 0
    },
];
let currentQuestion = 0;
let score = 0;

const questionElement = document.getElementById('question');
const optionsElement = document.getElementById('options');
const submitButton = document.getElementById('submit-btn');
const resultContainer = document.getElementById('result-container');
const scoreElement = document.getElementById('score');

function initializeQuiz() {
    loadQuestion();
}
function loadQuestion() {
    const currentQuiz = quizData[currentQuestion];
    questionElement.textContent = currentQuiz.question;
    optionsElement.innerHTML = '';
    currentQuiz.options.forEach((option, index) => {
    const li = document.createElement('li');
    const input = document.createElement('input');
    const label = document.createElement('label');

    input.type = 'radio';
    input.name = 'option';
    input.value = index;
    input.id = `option${index}`;

    label.textContent = option;
    label.htmlFor = `option${index}`;

    li.appendChild(input);
    li.appendChild(label);
    optionsElement.appendChild(li);
});
}
function checkAnswer() {
    const selectedOption = document.querySelector('input[name="option"]:checked');

    if (selectedOption) {
        const selectedIndex = parseInt(selectedOption.value);
        const currentQuiz = quizData[currentQuestion];

        if (selectedIndex === currentQuiz.answer) {
        score++;
        }

        currentQuestion++;

        if (currentQuestion < quizData.length) {
        loadQuestion();
        } else {
        showResult();
        }
}
}
function showResult() {
    document.getElementById('quiz-container').style.display = 'none';
    resultContainer.style.display = 'block';
    scoreElement.textContent = `Your Score: ${score}/${quizData.length}`;
}
submitButton.addEventListener('click', checkAnswer);
initializeQuiz();
