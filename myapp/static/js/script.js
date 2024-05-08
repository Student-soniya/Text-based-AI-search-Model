document.addEventListener('DOMContentLoaded', function() {
    var chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } else {
        console.error("Element '#chat-container' not found.");
    }
});

