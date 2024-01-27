document.addEventListener('DOMContentLoaded', function () {
    const topics = document.querySelectorAll('.topic-item');

    console.log('topic before ',topics )
    topics.forEach(topic => {
       // console.log('topic ', topic)
        topic.addEventListener('click', function () {
            console.log('on click ')
            topics.forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
            const topicName = this.querySelector('.topic-title').textContent;
            const topicDescription = this.querySelector('.topic-description').textContent;
            console.log('topic Name ', topicName)
            console.log('topic Description', topicDescription)
            fetch($SCRIPT_ROOT + '/fetch_prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topicName: topicName, topicDescription: topicDescription }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); 
                 // Scrape chatbox
                scrapeChat();
                // Start conversation with hidden prompt:
                startConversation();
            })
            .catch(error => console.error('Error:', error));
        });

        // Add an event listener to the delete icon
        const deleteIcon = topic.querySelector('.fa-trash');
        if (deleteIcon) {
            deleteIcon.addEventListener('click', function(event) {
                // Prevent the click from triggering the prompt selection
                event.stopPropagation();

                const topicName = this.getAttribute('data-topic-name');
                deletePrompt(topicName, topic);
            });
        }
        // Add an event listener to the delete icon
    });
});

function scrapeChat() {
    // Select the div with the class 'chatbox__messages'
    const chatboxMessages = document.querySelector('.chatbox__messages');

    // Check if the element exists
    if (chatboxMessages) {
        // Remove all child elements
        while (chatboxMessages.firstChild) {
            chatboxMessages.removeChild(chatboxMessages.firstChild);
        }
    } else {
        console.log('Element with class chatbox__messages not found.');
    }
}

function startConversation() {
    // prompt gpt to start conversation
    const prompt = "Let's start: Act as an english teacher to achieve the goal in the system prompt. Lead the conversation and correct the student if they say something wrong. Make sure to keep the conversation on track.";
    chatbox.get_response(prompt, chatbox.args.chatBox);
}

function deletePrompt(promptName, promptElement) {
    // Call the Flask endpoint to delete the prompt
    fetch($SCRIPT_ROOT + '/delete_prompt_template/' + encodeURIComponent(promptName), {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // Remove the prompt element from the DOM
            promptElement.remove();
        } else {
            console.error('Failed to delete prompt');
        }
    })
    .catch(error => console.error('Error:', error));
}