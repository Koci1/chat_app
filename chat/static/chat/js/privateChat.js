
import { appendMessage, appendSystemMessage, createPrivateChatBox } from "./ui.js";




let chatWrapper = document.querySelector("#chat-wrapper")
export function startPrivateChat(otherUser, myUsername, privateSockets) {
    if (myUsername === otherUser || privateSockets[otherUser]) return;

    const privatews = new WebSocket(`ws://${window.location.host}/ws/private/${myUsername}/${otherUser}/`);
    privateSockets[otherUser] = privatews;

    let chatBox = document.getElementById(`private_chat_${otherUser}`);
    if (!chatBox) {
        chatBox = createPrivateChatBox(otherUser, privatews, privateSockets);
        chatWrapper.appendChild(chatBox)
    }

    const messagesDiv = chatBox.querySelector(".messages");

    // privatews.onopen = () => console.log("Privatni chat sa", otherUser, "otvoren");

    privatews.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if(data.type === "info_message"){
            showMessage(data.message)
        }
        else if (data.sender && data.message) {
            showMessage(data.message,data.sender)
        }


    };

    function showMessage(message,sender = null){
        const p = document.createElement("p");
        p.style.whiteSpace = "normal"
        p.style.wordBreak = 'break-word'
        if(sender){
            p.textContent = `${sender}: ${message}`;
            if(sender == myUsername){
                p.classList.add("private-owner-message")
            }else{
                p.classList.add("private-message")
            }
        }else{
            p.textContent = `${message}`;
            
        }
        messagesDiv.appendChild(p);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    privatews.onclose = () => {
        appendSystemMessage(`Private chat with ${otherUser} has ended.`)
        delete privateSockets[otherUser];
        chatBox.remove();
        
        const remainingChats = Object.keys(privateSockets);
        remainingChats.forEach((user, index) => {
            const box = document.getElementById(`private_chat_${user}`);
            if (box) box.style.right = (index * 220 + 10) + "px";
        });
    };

    privatews.onerror = (err) => console.error("Greška u privatnom chatu:", err);
}
