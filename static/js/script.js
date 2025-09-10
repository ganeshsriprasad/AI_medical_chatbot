document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("user-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    appendMessage(userInput, "user-message");
    document.getElementById("user-input").value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        typeMessage(data.response);
    });
}

function appendMessage(text, className) {
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");
    messageElement.classList.add(className);
    messageElement.textContent = text;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function typeMessage(text) {
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");
    messageElement.classList.add("bot-message");
    chatBox.appendChild(messageElement);

    let words = text.split(" ");
    let i = 0;

    function showNextWord() {
        if (i < words.length) {
            messageElement.textContent += (i === 0 ? "" : " ") + words[i];
            i++;
            setTimeout(showNextWord, 100);
        }
    }
    showNextWord();
}
