class Chatbox{
    constructor() {
        this.args = {
            // openButton: document.querySelector(".chatbox__button"),
            chatBox: document.querySelector(".chatbox__support"),
            sendButton: document.querySelector(".send__button")
        }
    
        this.state = false;
        this.messages = [];
        this.chatbotMessageCount = 0;

    }

    display() {

        const {openButton, chatBox, sendButton} = this.args;
        // openButton.addEventListener('click',  () => this.toggleState(chatBox))
        sendButton.addEventListener('click',  () => this.onSendButton(chatBox))

        const node = chatBox.querySelector("input");
        node.addEventListener("keyup",  ({key}) => {
            if (key === "Enter"){
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox){

        this.state = !this.state;

        //show or hide the box
        if(this.state){
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    get_response(text1, chatbox){
        return fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = {name: "Chatbot", message: r.answer};
            this.messages.push(msg2);
            console.log('Messages ',this.messages);
            this.updateChatText(chatbox);
    
            if(r.end === 1){
                this.messages = []
                this.updateChatText(chatbox)
                setTimeout(2000)
            }
            console.log(msg2);
            return(msg2);
            
        }).catch((error) => {
            console.error('Error: ', error);
            //this.updateChatText(chatbox)  ? why
            textField.value = ''
        });
    }
    
    

    onSendButton(chatbox){
        var textField =  chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === ""){
            return;
        }

        let msg1 = {name: "User", message: text1}
        this.messages.push(msg1);
        this.updateChatText(chatbox)
        textField.value = ''

        this.get_response(text1, chatbox)
    }

    updateChatText(chatbox){    
        var html = '';
        const newMessage = this.messages[this.messages.length - 1]
        if (newMessage.name === "Chatbot") {
            console.log('First if');
            html += '<div class="messages__item--visitor"><i class="fa-solid fa-brain"></i><div class="messages__item_chatbot_text">' + newMessage.message + '</div></div>'
        } else {
            console.log('else');               
            html += '<div class="messages__item messages__item--operator">' + newMessage.message + '</div>'
        }
        this.chatbotMessageCount++;
        console.log('chatbot count ',this.chatbotMessageCount);
        // if (this.chatbotMessageCount === 5) {
        //     this.showPopup();
        // }

        const chatmessages = chatbox.querySelector('.chatbox__messages');
        //  console.log(chatmessages.innerHTML);
        chatmessages.innerHTML += html;
        chatmessages.scrollTop = chatmessages.scrollHeight;
    }

    // showPopup() {
    //     // Assuming you have a pop-up element with id 'popup'
    //     const popup = document.getElementById('popup');
    //     if (popup) {
    //         popup.classList.remove('hidden');
    //     }
    // }
    
    // closePopup() {
    //     const popup = document.getElementById('popup');
    //     if (popup) {
    //         popup.classList.add('hidden');
    //     }
    // }

}

const chatbox = new Chatbox();
chatbox.display();

// Attach chatbox to the global window object
window.chatbox = chatbox;
