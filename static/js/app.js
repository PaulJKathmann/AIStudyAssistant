class Chatbox{
    constructor() {
        this.args = {
            // openButton: document.querySelector(".chatbox__button"),
            chatBox: document.querySelector(".chatbox__support"),
            sendButton: document.querySelector(".send__button")
        }
        this.messageCounter = 0;
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
        // Parse Markdown to HTML
        const messageHtml = marked.parse(newMessage.message);


        if (newMessage.name === "Chatbot") {
            console.log('First if');
            html += '<div class="messages__item--visitor"><i class="fa-solid fa-brain"></i><div class="messages__item_chatbot_text">' + messageHtml + '</div></div>'
        } else {
            console.log('else');               
            html += '<div class="messages__item messages__item--operator">' + messageHtml + '</div>'
        }
        this.messageCounter++;

        // Check if counter is 4 and display popup
        if (this.messageCounter === 4) {
            html = html+this.displayPopup();
            this.messageCounter = 0; // Reset the counter
        }

        const chatmessages = chatbox.querySelector('.chatbox__messages');
        //  console.log(chatmessages.innerHTML);
        chatmessages.innerHTML += html;
        chatmessages.scrollTop = chatmessages.scrollHeight;
        
    }

    displayPopup() {
        // Create a new div element for the popup
        console.log('inside display popup');
        let popup = document.createElement("div");

        // Set the content of the popup
        popup.innerHTML = `
        <div class="popup alert alert-dismissible fade show" role="alert">
            Congratulations! You unlocked a new Pennimal
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`;

        // Add class for styling
        popup.classList.add("chatbox-popup");

        // Append the popup to the body
       // document.body.appendChild(popup);
        return popup.innerHTML;
    }

}

const chatbox = new Chatbox();
chatbox.display();

// Attach chatbox to the global window object
window.chatbox = chatbox;
