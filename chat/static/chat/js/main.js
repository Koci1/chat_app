// chat/static/chat/js/main.js
import { initChat } from "./globalChat.js";
import { messagesEl } from "./ui.js";

const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');

initChat(messageInput, messageForm);
