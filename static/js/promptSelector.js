document.addEventListener('DOMContentLoaded', function () {
    const topics = document.querySelectorAll('.topic-item');

    // Insert the course_code into the .topic-selection-header element
    const courseCodeElement = document.querySelector('.topic-selection-header');
    if (courseCodeElement) {
        // Get course_code from URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const course_code = urlParams.get('course_code');

        // Set the text content of the element
        courseCodeElement.textContent = course_code;
    }

    console.log('topic before ',topics )
    topics.forEach(topic => {
       // console.log('topic ', topic)
        topic.addEventListener('click', function () {
            console.log('on click ')
            topics.forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
            const topicName = this.querySelector('.topic-title').textContent;
            console.log("topic name", topicName);
            //const topicDescription = this.querySelector('.topic-description').textContent;
            //console.log("topic description", topicDescription);
            // Get course_code from URL parameters
            const urlParams = new URLSearchParams(window.location.search);
            const course_code = urlParams.get('course_code');
            console.log('Course Code:', course_code);  // Log the course code for debugging

            fetch($SCRIPT_ROOT + '/fetch_prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topicName: topicName, course_code: course_code }),
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
    const prompt = "Let's start: Act as an teaching assistant for a computer science student to achieve the goal in the system prompt.";
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