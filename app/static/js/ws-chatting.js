let token = localStorage.getItem("jpn_quiz_access_token");

let userEmail = String(Date.now());
document.getElementById("ws-id").innerText = userEmail;

let websocketScheme = (document.location.protocol === 'http:') ? 'ws' : 'wss';
let ws_url = `${websocketScheme}://${document.location.host}/ws-endpoint?token=${token}&user-id=${userEmail}`;
let ws = new WebSocket(ws_url);

// let userEmail = localStorage.getItem("user_email");


ws.onmessage = function (event) {
    let messages = document.getElementById('messages');
    let message = document.createElement('li');
    let data = JSON.parse(event.data);
    let content = document.createTextNode(data.message);
    let messageHeader = "";
    if (!data.message) {
        return;
    }
    if (data.message_type === 'list'){
        let chattingUsers = document.getElementById('chatting-users-div');
            while (chattingUsers.firstChild) {
                chattingUsers.removeChild(chattingUsers.firstChild);
            }
        data.message.forEach((elem)=>{
            let node = createUserName(elem);
            chattingUsers.append(node);
        });
        return;
    }
    if (data.message_type === 'message'){
        if (data.sender === userEmail){
            messageHeader = document.createTextNode("Your Message"+ " : ");
        }else{
            messageHeader = document.createTextNode(data.sender + " : ");
        }
    }
    if (data.message_type === 'whisper'){
        if (data.sender === userEmail){
            messageHeader = document.createTextNode("Your Whisper"+ " : ");
        }else{
            messageHeader = document.createTextNode(data.sender + " Whisper : ");
        }
    }
    if (data.message_type ==='alert'){
        processAlert(data);
    }

    message.append(messageHeader, content);
    messages.appendChild(message);
    document.querySelector("#messages-div").scrollTop =
        document.querySelector("#messages-div").scrollHeight;

};

function createUserName(client_id){
    let node = document.createElement('div');
    node.textContent = client_id;
    if(client_id === userEmail){
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
        let node = createUserName(data.sender);
        if (!document.getElementById(node.id)) {
            document.getElementById('chatting-users-div').append(node);
        }
    }
    else if(data.detail ==='leave'){
        if(document.getElementById(data.sender)) {
            document.getElementById(data.sender).remove();
        }
        if(data.sender === userEmail){
            ws.close();
        }
    }
}

function sendMessage(event) {
    let input = document.getElementById("messageText");
    let target = document.getElementById("sendTo");
    let messageType = target.value ? 'whisper' : 'message';
    let message= {
            message_type: messageType,
            sender: userEmail,
            message: input.value
        };
    if (target.value){
        message.receiver = target.value;
    }
    ws.send(JSON.stringify(message));
    input.value = '';
    event.preventDefault();
}

// let my_client_id = String(Date.now());
// document.querySelector("#ws-id").textContent = String(my_client_id);
// let websocketScheme = (document.location.protocol === 'http:') ? 'ws' : 'wss';
// let ws_send = new WebSocket(`${websocketScheme}://${document.location.host}/chatting/${my_client_id}/send`,);
// let ws_receive = new WebSocket(`${websocketScheme}://${document.location.host}/chatting/${my_client_id}/receive`,);
// ws_receive.onclose = function () {
//     ws_receive.send("disconnected");
// };
//
// ws_receive.onmessage = function (event) {
//     let messages = document.getElementById('messages');
//     let message = document.createElement('li');
//     let data = JSON.parse(event.data);
//     /**
//      * @param data
//      * @param data.client_id
//      * @param data.message
//      * @param data.type
//      * @param data.sender
//      * @param data.detail
//      * **/
//     let content = document.createTextNode(data.message);
//     let messageHeader = "";
//     if (data.type === 'keepalive'){
//         return;
//     }
//     if (data.type === 'list'){
//         data.message.forEach((elem)=>{
//             let node = createUserName(elem);
//             document.getElementById('chatting-users-div').append(node);
//         });
//         return;
//     }
//     if (data.type === 'whisper'){
//         if (data.sender === my_client_id){
//             messageHeader = document.createTextNode("to " + data.sender + " : ");
//         }else{
//             messageHeader = document.createTextNode("from " + data.sender + " : ");
//         }
//
//     }
//
//     if (data.type === 'message'){
//         if (data.sender === my_client_id){
//             messageHeader = document.createTextNode("Your Message"+ " : ");
//         }else{
//             messageHeader = document.createTextNode(data.sender + " : ");
//         }
//     }
//     if (data.type === 'alert') {
//         processAlert(data);
//         messageHeader = data.sender+" ";
//     }
//     message.append(messageHeader, content);
//     messages.appendChild(message);
//     document.querySelector("#messages-div").scrollTop =
//         document.querySelector("#messages-div").scrollHeight;
// };
//
// ws_send.onopen = ()=>{
//     let a = function () {
//         setTimeout(a,40000);
//         ws_send.send(JSON.stringify({
//             keepalive: true
//         }));
//     };
//     a();
// };
//
// function createUserName(client_id){
//     let node = document.createElement('div');
//     node.textContent = client_id;
//     if(client_id === my_client_id){
//         node.textContent += '(나)';
//     }
//     node.id = client_id;
//     node.addEventListener('click',()=>{
//         document.getElementById('sendTo').value = client_id;
//     });
//     return node;
// }
//
// function processAlert(data){
//     if (data.detail === 'enter'){
//         let node = createUserName(data.sender);
//         if (!document.getElementById(node.id)) {
//             document.getElementById('chatting-users-div').append(node);
//         }
//     }
//     else if(data.detail ==='leave'){
//         if(document.getElementById(data.sender)) {
//             document.getElementById(data.sender).remove();
//         }
//         if(data.sender === my_client_id){
//             ws_receive.close();
//         }
//     }
// }
//
// function sendMessage(event) {
//     let input = document.getElementById("messageText");
//     let target = document.getElementById("sendTo");
//     ws_send.send(
//         JSON.stringify({
//             type: "message",
//             sender: my_client_id,
//             message: input.value,
//             receiver: target.value
//         }));
//     input.value = '';
//     event.preventDefault();
// }
