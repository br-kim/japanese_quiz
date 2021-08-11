let my_client_id = String(Date.now());
document.querySelector("#ws-id").textContent = String(my_client_id);
let ws = new WebSocket(`ws://127.0.0.1:8000/chatting/${my_client_id}`);
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
     * @param data.detail
     * **/
    let content = document.createTextNode(data.message);
    let messageHeader = "";
    if (data.type === 'list'){
        console.log(data.message);
        data.message.forEach((elem)=>{
            let node = createUserName(elem);
            document.getElementById('chatting-users-div').append(node);
        });
        return;
    }
    if (data.type === 'whisper'){
        messageHeader = document.createTextNode("from " + data.sender + " : ");
    }

    if (data.type === 'message'){
        if (data.client_id === my_client_id){
            messageHeader = document.createTextNode("Your Message"+ " : ");
        } else if (data.sender === my_client_id){
            messageHeader = document.createTextNode("to " + data.client_id + " : ");
        } else {
            messageHeader = document.createTextNode(data.client_id + " : ");
        }
    }
    if (data.type === 'alert') {
        processAlert(data);
        messageHeader = data.client_id+" ";
    }
    message.append(messageHeader, content);
    messages.appendChild(message);
    document.querySelector("#messages-div").scrollTop =
        document.querySelector("#messages-div").scrollHeight;
};

function createUserName(client_id){
    let node = document.createElement('div');
    node.textContent = client_id;
    if(client_id === my_client_id){
        node.textContent += '(나)';
    }
    node.id = client_id;
    node.addEventListener('click',()=>{
        document.getElementById('sendTo').value = client_id;
    });
    return node;
}

function processAlert(data){
    if (data.detail === 'enter'){
        let node = createUserName(data.client_id);
        if (!document.getElementById(node.id)) {
            document.getElementById('chatting-users-div').append(node);
        }
    }
    else if(data.detail ==='leave'){
        document.getElementById(data.client_id).remove();
    }
}

function sendMessage(event) {
    let input = document.getElementById("messageText");
    let target = document.getElementById("sendTo");
    ws.send(
        JSON.stringify({
            sender: my_client_id,
            message: input.value,
            receiver: target.value
        }));
    input.value = '';
    event.preventDefault();
}
