let ws = null;

function connectToChat(chatName) {
    ws = new WebSocket(`ws://localhost:8000/ws/${chatName}`);
    ws.onmessage = function (event) {
        const messages = document.getElementById("messages");
        const li = document.createElement("li");
        li.textContent = event.data;
        messages.appendChild(li);
        messages.scrollTop = messages.scrollHeight; // Прокрутка вниз
    };
}

function sendMessage() {
    const chatName = document.getElementById("chat_name").value.trim();
    const username = document.getElementById("username").value.trim();
    const message = document.getElementById("message").value.trim();

    if (!chatName || !username || !message) {
        alert("Все поля должны быть заполнены!");
        return;
    }

    if (!ws || ws.readyState !== WebSocket.OPEN) {
        connectToChat(chatName);
    }

    ws.send(`${username}: ${message}`);
    document.getElementById("message").value = ""; // Очистить поле ввода
}
