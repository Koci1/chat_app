// chat/static/chat/js/ui.js
export const messagesEl = document.getElementById('messages');
export const userListEl = document.getElementById('user-list');

export function appendMessage(user, message, myUsername) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message');
    messageEl.innerHTML = `<span class="author">${user}:</span> ${message}`;
    messagesEl.appendChild(messageEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    if (user === myUsername) messageEl.style.backgroundColor = 'black';
}

export function appendSystemMessage(message) {
    const systemMessageEl = document.createElement('div');
    systemMessageEl.classList.add('system-message');
    systemMessageEl.textContent = message;
    messagesEl.appendChild(systemMessageEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

export function updateUserList(users, startPrivateChatCallback) {
    userListEl.innerHTML = '';
    users.forEach(username => {
        const userItem = document.createElement('li');
        userItem.textContent = username;
        userItem.onclick = () => startPrivateChatCallback(username);
        userListEl.appendChild(userItem);
    });
}

export function createPrivateChatBox(otherUser, privatews, privateSockets) {
    const chatBoxId = `private_chat_${otherUser}`;
    const chatBox = document.createElement("div");
    chatBox.id = chatBoxId;
    chatBox.classList.add("mini-chat");
    chatBox.style.position = "fixed";
    chatBox.style.bottom = "10px";
    
    const chatUsers = Object.keys(privateSockets);
    chatBox.style.right = (chatUsers.indexOf(otherUser) * 220 + 10) + "px";

    chatBox.style.width = "200px";
    chatBox.style.height = "250px";
    chatBox.style.border = "1px solid #ccc";
    chatBox.style.background = "#f9f9f9";
    chatBox.style.padding = "5px";
    chatBox.style.display = "flex";
    chatBox.style.flexDirection = "column";

    chatBox.innerHTML = `
        <h4 style="margin:0; font-size:14px;">Chat sa ${otherUser}</h4>
        <div class="messages" style="flex:1; overflow-y:auto; border:1px solid #ddd; padding:2px; margin:2px 0;"></div>
        <input type="text" placeholder="Poruka..." style="flex:none;" />
        <button style="flex:none;">Pošalji</button>
    `;

    document.body.appendChild(chatBox);

    const input = chatBox.querySelector("input");
    const btn = chatBox.querySelector("button");

    btn.onclick = () => {
        const msg = input.value.trim();
        if (msg) {
            privatews.send(JSON.stringify({ message: msg }));
            input.value = "";
        }
    };

    return chatBox;
}
