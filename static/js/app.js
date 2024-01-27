class Chatbox{
    constructor() {
        this.args = {
            // openButton: document.querySelector(".chatbox__button"),
            chatBox: document.querySelector(".chatbox__support"),
            sendButton: document.querySelector(".send__button")
        }
    
        this.state = false;
        this.messages = [];

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
            let msg2 = {name: "Chatbot", message: r.answer, voice_speed: r.voice_speed};
            
            // Check the state of the toggle
            const isVoiceThenText = document.getElementById('voiceThenTextToggle').checked;
          //  console.log("isvoi "+isVoiceThenText);
            if(isVoiceThenText){
                // If the toggle is checked, voice first then text
                convertTextToSpeech(r.answer, r.voice_speed, () => {
                    this.messages.push(msg2);
                    this.updateChatText(chatbox);
                });
            } else {
                // If the toggle is not checked, text first then voice
                this.messages.push(msg2);
                console.log('Messages ',this.messages);
                this.updateChatText(chatbox);
                convertTextToSpeech(r.answer, r.voice_speed);
            }
    
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
        const voiceOnly = document.getElementById('voiceOnlyToggle').checked;
    
        if (!voiceOnly) { // Check if voice-only mode is off
            var html = '';
            const newMessage = this.messages[this.messages.length - 1]
    
            if (newMessage.name === "Chatbot") {
                console.log('First if');
                html += '<div class="messages__item--visitor"><i class="fa fa-robot chat-icon"></i><div class="messages__item_chatbot_text">' + newMessage.message + '</div></div>'
            } else {
                console.log('else');               
                html += '<div class="messages__item messages__item--operator">' + newMessage.message + '</div>'
            }
    
            const chatmessages = chatbox.querySelector('.chatbox__messages');
          //  console.log(chatmessages.innerHTML);
            chatmessages.innerHTML += html;
            chatmessages.scrollTop = chatmessages.scrollHeight;
        }
    }

}

const chatbox = new Chatbox();
chatbox.display();

// Attach chatbox to the global window object
window.chatbox = chatbox;
