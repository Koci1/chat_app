// chat/static/chat/js/globalChat.js
import { appendMessage, appendSystemMessage, updateUserList } from "./ui.js";
import { startPrivateChat } from "./privateChat.js";

export let liveMessages = []
export let myUsername = " ";
export const privateSockets = {};

export const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

export function initChat(messageInput, messageForm) {
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({ message }));
            messageInput.value = '';
        }
    });

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        switch(data.type) {
            case 'chat_message':
                appendMessage(data.user, data.message, myUsername);
                liveMessages.push(data);
                break;
            case 'info_message':
                appendSystemMessage(data.message);
                liveMessages.push(data);
                break;
            case 'users_list':
                updateUserList(data.users, (user) => {
                    startPrivateChat(user, myUsername, privateSockets);
                    chatSocket.send(JSON.stringify({
                        type: "private_chat_open",
                        from: myUsername,
                        to: user
                    }));
                });
                break;
            case 'username_recieve':
                myUsername = data.user;
                break;
            case 'open_chat':
                startPrivateChat(data.init_user, myUsername, privateSockets);
                break;
        }
    };
}
