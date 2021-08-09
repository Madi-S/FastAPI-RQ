const username = prompt('Enter your username:', Date.now()).toString().trim()
const ws = new WebSocket(`ws://localhost:5057/ws/${roomId}/${username}`)

const messageInput = document.getElementById('message-input')
const sendMessageBtn = document.getElementById('message-submit')
const messagesCollection = document.getElementById('message-collection')
sendMessageBtn.addEventListener('click', sendMessage)

function sendMessage(event) {
    const message = generateJSONMessage()
    ws.send(message)
    messageInput.value = ''
    event.preventDefault()
}

function appendMessage(message) {
    html = `
    <li class="collection-item">
            <div><b>${message.author}:</b> ${message.text}
                <a class="secondary-content"><i class="material-icons">send</i></a>
            </div>
        </li>
    `.trim()
    messagesCollection.insertAdjacentHTML('beforeend', html)
}

function generateJSONMessage() {
    const message = {}
    message.author = username
    message.text = messageInput.value.trim()
    return JSON.stringify(message)
}

ws.onmessage = function (event) {
    const message = JSON.parse(JSON.parse(event.data))
    appendMessage(message)
}
