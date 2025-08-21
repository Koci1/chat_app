import { appendMessage, appendSystemMessage, messagesEl } from "./ui.js";
import { myUsername } from './globalChat.js'
import { liveMessages } from "./globalChat.js";
let buffer = [];
let next = "";
let pageStart = 1
let isLoading = false
let urls = "/api/messages/"
let deletedStart = 0;

async function fetchMessages(url,direction) {
    // if(buffer.length == 3 && url){
    //     if(direction === "up"){
    //         buffer.pop()
    //         deletedStart++
    //     }
    //     else{
    //         buffer.shift()
    //     }
    // }
    if(url){
    await fetch(url)
        .then(response => response.json()
            .then(data => {
                if(direction == "down"){
                    buffer.push(data.results)
                }else{
                    buffer.unshift(data.results)
                    next = data.next
                }
                renderMessage()
            }))
        }
}


fetchMessages(`${urls}?page=${pageStart}`,"up")


function chatArraysEqual(arr1, arr2) {
    if (arr1.length !== arr2.length) return false;

    for (let i = 0; i < arr1.length; i++) {
        const obj1 = arr1[i];
        const obj2 = arr2[i];

        // Provjera svih ključeva u objektu
        for (let key in obj1) {
            if (obj1[key] !== obj2[key]) return false;
        }

        // Provjeri da obj2 nema dodatnih ključeva
        for (let key in obj2) {
            if (!(key in obj1)) return false;
        }
    }
    return true;
}

let copy = []

function renderMessage(){
    // Zadrži trenutnu poziciju scrolla prije rendera
    const scrollTopBefore = messagesEl.scrollTop;
    const scrollHeightBefore = messagesEl.scrollHeight;
    copy = [...liveMessages]
    
    // Renderuj poruke
    messagesEl.innerHTML = ''; // ili ukloni ako dodaješ na vrh bez brisanja
    buffer.forEach(obj => {
        let copy = [...obj];
        copy.reverse().forEach(msg => {
            appendMessage(msg.owner, msg.content, myUsername);
        });
    });

    if(chatArraysEqual(copy, liveMessages)){
        copy.forEach(msg=>{
            if(msg.type == "chat_message"){
                appendMessage(msg.user,msg.message,myUsername)
            }else if(msg.type=="info_message")
                appendSystemMessage(msg.message)
        })
    }


    // Podesi scroll da ostane na istom mjestu
    const scrollHeightAfter = messagesEl.scrollHeight;
    messagesEl.scrollTop = scrollTopBefore + (scrollHeightAfter - scrollHeightBefore);
}

messagesEl.addEventListener("scroll", () => {
    const scrollTop = messagesEl.scrollTop;
    const scrollHeight = messagesEl.scrollHeight;
    const clientHeight = messagesEl.clientHeight;
    // Ako je korisnik blizu vrha (npr. gornja polovica)
    if (scrollTop < 200 && next && !isLoading) {
        isLoading = true
        fetchMessages(next,"up").finally(()=>{
            isLoading = false
        }); 
    }

});





