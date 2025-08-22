// chat/static/chat/js/ui.js
export const messagesEl = document.getElementById('messages');
export const userListEl = document.getElementById('user-list');

export function appendMessage(user, message, myUsername) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message');
    messageEl.innerHTML = `<p class="author">${user}</p><p>:</p><p class="content-message">${message}</p>`;
    messagesEl.appendChild(messageEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    if (user === myUsername) messageEl.classList.add("owner");
}

export function appendSystemMessage(message) {
    const systemMessageEl = document.createElement('div');
    systemMessageEl.classList.add('system-message');
    systemMessageEl.textContent = message;
    messagesEl.appendChild(systemMessageEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("minimize-chat")) {
        const chatBox = e.target.closest(".chat-box");
        const content = chatBox.querySelector(".chat-content");

        const isHidden = getComputedStyle(content).display === "none";

        if (isHidden) {
            content.style.display = "flex";
            e.target.textContent = "–"; 
        } else {
            content.style.display = "none";
            e.target.textContent = "+"; 
        }
    }
});


export function updateUserList(users, startPrivateChatCallback) {
    userListEl.innerHTML = '';
    users.forEach(username => {
        const userItem = document.createElement('li');
        userItem.classList.add("user-list-item");

        const icon = document.createElement('i');
        icon.classList.add('fa-solid', 'fa-circle', 'user-icon'); // font awesome user icon
        icon.style.marginRight = '8px';

        // tekst korisnika
        const text = document.createTextNode(username);

        // dodaj sve u li
        userItem.appendChild(text);
        userItem.appendChild(icon);

        userItem.onclick = () => startPrivateChatCallback(username);
        userListEl.appendChild(userItem);
    });
}

// export function createPrivateChatBox(otherUser, privatews, privateSockets) {
//     const chatBoxId = `private_chat_${otherUser}`;
//     const chatBox = document.createElement("div");
//     chatBox.id = chatBoxId;
//     chatBox.classList.add("mini-chat");
//     chatBox.style.position = "fixed";
//     chatBox.style.bottom = "10px";

//     const chatUsers = Object.keys(privateSockets);
//     chatBox.style.right = (chatUsers.indexOf(otherUser) * 220 + 10) + "px";

//     chatBox.style.width = "200px";
//     chatBox.style.height = "250px";
//     chatBox.style.border = "1px solid #ccc";
//     chatBox.style.background = "#f9f9f9";
//     chatBox.style.padding = "5px";
//     chatBox.style.display = "flex";
//     chatBox.style.flexDirection = "column";

//     chatBox.innerHTML = `
//         <h4 style="margin:0; font-size:14px;">Chat sa ${otherUser}</h4>
//         <div class="messages" style="flex:1; overflow-y:auto; border:1px solid #ddd; padding:2px; margin:2px 0;"></div>
//         <input type="text" placeholder="Poruka..." style="flex:none;" />
//         <button style="flex:none;">Pošalji</button>
//     `;

//     document.body.appendChild(chatBox);

//     const input = chatBox.querySelector("input");
//     const btn = chatBox.querySelector("button");

//     btn.onclick = () => {
//         const msg = input.value.trim();
//         if (msg) {
//             privatews.send(JSON.stringify({ message: msg }));
//             input.value = "";
//         }
//     };

//     return chatBox;
// }


export function createPrivateChatBox(otherUser, privatews, privateSockets) {
    const chatBoxId = `private_chat_${otherUser}`;
    const chatBox = document.createElement("div");
    chatBox.id = chatBoxId;
    chatBox.classList.add("mini-chat");
    chatBox.classList.add("chat-box"); // OVO JE BITNO ZA MINIMIZE

    const chatUsers = Object.keys(privateSockets);
    chatBox.style.right = (chatUsers.indexOf(otherUser) * 220 + 10) + "px";

    chatBox.innerHTML = `
    <div class="chat-header" style="display:flex; justify-content:space-between; align-items:center; background-color:#1E1E2F; padding:5px;">
        <h4 style="margin:5px 10px; font-size:14px; color:white;">${otherUser}</h4>
        <div>
            <button class="minimize-chat" style="margin-right:8px; background:transparent; font-size:15px; color:white; border:none; cursor:pointer;">_</button>
            <button class="close-chat" style="background:transparent; font-size:15px; color:white; border:none; cursor:pointer;">X</button>
        </div>
    </div>
    <div class="chat-content" style="display:flex; flex-direction:column; height:200px;">
        <div class="messages" style="flex:1; overflow-y:auto; padding:4px; margin:2px 0; background-color:#2A2A40; color:white; font-size:13px; border-radius:4px;"></div>
        <div style="display:flex; gap:5px; margin-top:5px;">
            <input type="text" placeholder="Poruka..." style="flex:1; color:white; border:none; background-color:#2A2A40; padding:5px; border-radius:4px;" />
            <button class="send" style="background-color:#2A2A40; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">Pošalji</button>
        </div>
    </div>
`;

    document.body.appendChild(chatBox);

    const input = chatBox.querySelector("input");
    const sendBtn = chatBox.querySelector(".send");
    const closeBtn = chatBox.querySelector(".close-chat");
    const minimizeBtn = chatBox.querySelector(".minimize-chat");

    sendBtn.onclick = () => {
        const msg = input.value.trim();
        if (msg) {
            privatews.send(JSON.stringify({ message: msg }));
            input.value = "";
        }
    };

    closeBtn.onclick = () => {
        if (privatews.readyState === WebSocket.OPEN) {
            privatews.close();
        }
        chatBox.remove();
    };
    return chatBox;
}

