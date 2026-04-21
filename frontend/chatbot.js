const sendButton = document.getElementById("sendButton");
const userInputField = document.getElementById("userInput");
const chatbox = document.getElementById("chatbox");
const loadingContainer = document.getElementById("loadingContainer");

sendButton.addEventListener("click", handleUserInput);
userInputField.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    handleUserInput();
  }
});

function handleUserInput() {
  const userInput = userInputField.value.trim();
  if (!userInput) return;

  // Display user message
  const userMessageDiv = document.createElement("div");
  userMessageDiv.classList.add("chat-message", "user-message");
  userMessageDiv.textContent = userInput;
  chatbox.appendChild(userMessageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;

  // Show loading
  loadingContainer.style.display = "block";
  userInputField.disabled = true;
  sendButton.disabled = true;

  // Fetch API call to Flask backend
  fetch("http://127.0.0.1:5004/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: userInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      const chatbotResponseDiv = document.createElement("div");
      chatbotResponseDiv.classList.add("chat-message", "chatbot-message");
      chatbotResponseDiv.textContent = data.response || "No response received.";
      chatbox.appendChild(chatbotResponseDiv);

      const chatbotMessageTail = document.createElement("div");
      chatbotMessageTail.classList.add("tail");
      chatbotResponseDiv.appendChild(chatbotMessageTail);

      chatbox.scrollTop = chatbox.scrollHeight;

      // Reset input
      userInputField.value = "";
      userInputField.disabled = false;
      sendButton.disabled = false;
      loadingContainer.style.display = "none";
      userInputField.focus();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
      userInputField.disabled = false;
      sendButton.disabled = false;
      loadingContainer.style.display = "none";
    });
}
