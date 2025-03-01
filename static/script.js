// script.js (Updated: Removed Loader Code)
document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();
    if (message === "") return;

    appendMessage("user", message);
    userInput.value = "";

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("bot", data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        appendMessage("bot", "Oops! Something went wrong. Please try again.");
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message-container", sender);

    const img = document.createElement("img");
    img.classList.add("avatar");
    img.src = sender === "bot" ? "/static/images/bot_icon.jpg" : "/static/images/user_icon.png";
    img.alt = sender === "bot" ? "Bot" : "User";

    const text = document.createElement("p");
    text.textContent = message;

    messageContainer.style.opacity = "0";
    setTimeout(() => { messageContainer.style.opacity = "1"; }, 100);

    messageContainer.appendChild(img);
    messageContainer.appendChild(text);
    chatBox.appendChild(messageContainer);

    chatBox.scrollTop = chatBox.scrollHeight;
}

window.onload = function() {
    appendMessage("bot", "Hi, I'm Chatbot and I like to chat.");
    appendMessage("bot", "Please type lowercase English language to start a conversation. Type 'quit' to leave.");
};
