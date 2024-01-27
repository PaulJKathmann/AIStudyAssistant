document.addEventListener('DOMContentLoaded', function () {
    const prompts = document.querySelectorAll('.prompt-item');

    prompts.forEach(prompt => {
        prompt.addEventListener('click', function () {
            // Remove 'selected' class from all prompts
            prompts.forEach(p => p.classList.remove('selected'));
            // Add 'selected' class to clicked prompt
            this.classList.add('selected');

            // Send selected prompt to backend
            const promptName = this.querySelector('.prompt-title').textContent;
            const promptDescription = this.querySelector('.prompt-description').textContent;

            fetch($SCRIPT_ROOT + '/update_prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ promptName, promptDescription }),
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
        const deleteIcon = prompt.querySelector('.fa-trash');
        if (deleteIcon) {
            deleteIcon.addEventListener('click', function(event) {
                // Prevent the click from triggering the prompt selection
                event.stopPropagation();

                const promptName = this.getAttribute('data-prompt-name');
                deletePrompt(promptName, prompt);
            });
        }
        // Add an event listener to the delete icon
        const editIcon = prompt.querySelector('.edit_prompt_button');
        if (editIcon) {
            editIcon.addEventListener('click', function(event) {
                // Prevent the click from triggering the prompt selection
                event.stopPropagation();
            });
        }
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