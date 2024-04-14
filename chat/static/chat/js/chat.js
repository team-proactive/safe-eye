document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesDiv = document.getElementById('messages');
    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/');

    chatSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const message = data['message'];
        const messageElement = document.createElement('div');
        messageElement.innerText = message;
        messagesDiv.appendChild(messageElement);
    };

    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = messageInput.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    });
});