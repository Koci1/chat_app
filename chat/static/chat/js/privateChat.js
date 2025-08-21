// chat/static/chat/js/privateChat.js
import { createPrivateChatBox } from "./ui.js";

export function startPrivateChat(otherUser, myUsername, privateSockets) {
    if (myUsername === otherUser || privateSockets[otherUser]) return;

    const privatews = new WebSocket(`ws://${window.location.host}/ws/private/${myUsername}/${otherUser}/`);
    privateSockets[otherUser] = privatews;

    let chatBox = document.getElementById(`private_chat_${otherUser}`);
    if (!chatBox) {
        chatBox = createPrivateChatBox(otherUser, privatews, privateSockets);
    }

    const messagesDiv = chatBox.querySelector(".messages");

    privatews.onopen = () => console.log("Privatni chat sa", otherUser, "otvoren");

    privatews.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.sender && data.message) {
            const p = document.createElement("p");
            p.textContent = `${data.sender}: ${data.message}`;
            messagesDiv.appendChild(p);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    };

    privatews.onclose = () => {
        console.log("Privatni chat sa", otherUser, "zatvoren");
        delete privateSockets[otherUser];
        chatBox.remove();

        // pomjeri ostale chatove lijevo
        const remainingChats = Object.keys(privateSockets);
        remainingChats.forEach((user, index) => {
            const box = document.getElementById(`private_chat_${user}`);
            if (box) box.style.right = (index * 220 + 10) + "px";
        });
    };

    privatews.onerror = (err) => console.error("Greška u privatnom chatu:", err);
}
