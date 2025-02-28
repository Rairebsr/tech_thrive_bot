document.addEventListener("DOMContentLoaded", function () {
  let userInputField = document.getElementById("userInput");
  let chatbox = document.getElementById("chatbox");

  
  userInputField.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
          event.preventDefault();
          sendMessage();
      }
  });

  
  function sendMessage() {
      let userInput = userInputField.value.trim();
      if (userInput === "") return;

      
      let userMessage = `<div class='message user-message'>${userInput}</div>`;
      chatbox.innerHTML += userMessage;
      chatbox.scrollTop = chatbox.scrollHeight;

      
      fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userInput })
      })
      .then(response => response.json())
      .then(data => {
          let botMessage = `<div class='message bot-message'>${data.response}</div>`;
          chatbox.innerHTML += botMessage;
          chatbox.scrollTop = chatbox.scrollHeight;
      });

      // Clear input after sending
      userInputField.value = "";
  }

  // Attach sendMessage function to Send button
  document.getElementById("sendButton").addEventListener("click", sendMessage);
});

        function sendMessage() {
            let userInput = document.getElementById("userInput").value.trim();
            let chatbox = document.getElementById("chatbox");

            if (userInput === "") return;

            // Display user message
            let userMessage = `<div class='message user-message'>${userInput}</div>`;
            chatbox.innerHTML += userMessage;
            chatbox.scrollTop = chatbox.scrollHeight;

            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                let botMessage = `<div class='message bot-message'>${data.response}</div>`;
                chatbox.innerHTML += botMessage;
                chatbox.scrollTop = chatbox.scrollHeight;
            });

            document.getElementById("userInput").value = ""; 
        }
        function displayMessage(message, sender) {
          const chatBox = document.getElementById("chat-box");
          const messageElement = document.createElement("div");
          messageElement.classList.add(sender);
          
          if (message.includes("\n")) {
              messageElement.innerHTML = `<pre>${message}</pre>`;
          } else {
              messageElement.textContent = message;
          }
      
          chatBox.appendChild(messageElement);
          chatBox.scrollTop = chatBox.scrollHeight;
      }


        function sendMessage() {
            let userInput = document.getElementById("userInput").value.trim();
            let chatbox = document.getElementById("chatbox");

            if (userInput === "") return;

            let userMessage = `<div class='message user-message'>${userInput}</div>`;
            chatbox.innerHTML += userMessage;
            chatbox.scrollTop = chatbox.scrollHeight;

            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                let botMessage = `<div class='message bot-message'>${data.response}</div>`;
                chatbox.innerHTML += botMessage;
                chatbox.scrollTop = chatbox.scrollHeight;
            });

            document.getElementById("userInput").value = ""; 
        }
