document.addEventListener("DOMContentLoaded", function () {
    let userInputField = document.getElementById("userInput");
    let chatbox = document.getElementById("chatbox");
    let sendButton = document.getElementById("sendButton");

    // Listen for "Enter" key to send message
    userInputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    // Attach sendMessage function to Send button
   sendButton.addEventListener("click", sendMessage);

    // Function to send message
    function sendMessage() {
        let userInput = userInputField.value.trim();
        if (userInput === "") return;

        displayMessage(userInput, "user-message");

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => displayMessage(data.response, "bot-message"))
        .catch(error => console.error("Error:", error));

        userInputField.value = "";
    }

    // Function to display message in chatbox
    function displayMessage(message, senderClass) {
        let messageElement = document.createElement("div");
        messageElement.classList.add("message", senderClass);

        // Preserve formatting for multiline text (like bus schedules)
        if (message.includes("\n")) {
            messageElement.innerHTML = `<pre>${message}</pre>`;
        } else {
            messageElement.textContent = message;
        }

        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
