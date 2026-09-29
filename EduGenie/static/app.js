const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const status = document.getElementById("status");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");

const examples = {
    qa: "Which is the largest ocean?",
    explain: "Explain the Pythagoras theorem for a beginner.",
    quiz: "The water cycle describes how water moves through evaporation, condensation, precipitation, and collection.",
    summarize: "Paste a long educational paragraph here and EduGenie will turn it into concise revision notes.",
    learn: "SQL"
};

function renderText(text) {
    result.textContent = text || "No result returned.";
}

function renderQuiz(data) {
    result.innerHTML = "";
    (data.questions || []).forEach((item, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "quiz-question";
        const heading = document.createElement("h3");
        heading.textContent = `${index + 1}. ${item.question}`;
        wrapper.appendChild(heading);

        item.options.forEach(option => {
            const optionEl = document.createElement("div");
            optionEl.className = "option";
            optionEl.textContent = option;
            wrapper.appendChild(optionEl);
        });

        const answer = document.createElement("div");
        answer.className = "answer";
        answer.textContent = `Correct answer: ${item.correct_answer}`;
        wrapper.appendChild(answer);
        result.appendChild(wrapper);
    });
}

task.addEventListener("change", () => {
    inputText.placeholder = examples[task.value];
});

submitBtn.addEventListener("click", async () => {
    const text = inputText.value.trim();
    if (!text) {
        status.textContent = "Please enter a question, topic, or passage.";
        return;
    }

    const route = task.value === "learn" ? "/learn/recommendations" : `/${task.value}`;
    submitBtn.disabled = true;
    status.textContent = "Generating...";
    resultCard.classList.remove("hidden");
    result.textContent = "";

    try {
        const response = await fetch(route, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Request failed.");
        }

        if (task.value === "quiz") {
            renderQuiz(data);
        } else {
            renderText(data.result);
        }
        status.textContent = "Done.";
    } catch (error) {
        result.textContent = error.message;
        status.textContent = "Something went wrong.";
    } finally {
        submitBtn.disabled = false;
    }
});

copyBtn.addEventListener("click", async () => {
    await navigator.clipboard.writeText(result.innerText);
    status.textContent = "Result copied to clipboard.";
});

inputText.placeholder = examples[task.value];
