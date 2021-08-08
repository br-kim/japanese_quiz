let client_id = String(Date.now());
document.querySelector("#ws-id").textContent = String(client_id);
let ws = new WebSocket(`ws://127.0.0.1:8000/chatting/${client_id}`);
ws.onmessage = function (event) {
    let messages = document.getElementById('messages');
    let message = document.createElement('li');
    let data = JSON.parse(event.data);
    /**
     * @param data
     * @param data.client_id
     * @param data.message
     * @param data.type
     * @param data.sender
     * **/
    let content = document.createTextNode(data.message);
    let userId = "";
    if (data.client_id === client_id) {
        if (data.type === 'whisper'){
            userId = document.createTextNode("from " + data.sender);
        }else {
            userId = document.createTextNode("Your Message");
        }
    } else {
        userId = document.createTextNode(data.client_id);
    }
    if (data.type === 'alert') {
        message.append(data.client_id, " ", content);
    } else {
        message.append(userId, ": ", content);
    }
    messages.appendChild(message);
    document.querySelector("#messages").scrollTop =
        document.querySelector("#messages").scrollHeight;
};

function sendMessage(event) {
    let input = document.getElementById("messageText");
    let target = document.getElementById("sendTo");
    ws.send(
        JSON.stringify({
            sender: client_id,
            message: input.value,
            receiver: target.value
        }));
    input.value = '';
    event.preventDefault();
}
