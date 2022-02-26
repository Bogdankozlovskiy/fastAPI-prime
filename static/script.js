document.addEventListener("DOMContentLoaded", function (){
    function connect(){
        let socket = new WebSocket("ws://localhost:8000/web_socket")
        socket.onmessage = function (event){
            let response_data = JSON.parse(event.data)
            let message_text = document.createElement("h3")
            message_text.innerHTML = response_data['text']
            let message_container = document.querySelector("#message-container")
            message_container.append(message_text)
        }

        let submit_button = document.querySelector("#submit-button")
        submit_button.addEventListener("click", function (){
            let text_area = document.querySelector("[name=text]")
            socket.send(JSON.stringify({"text": text_area.value}))
            text_area.value = ""
        }, false)

        socket.onclose = function (){
            socket = null
            setTimeout(connect, 1000)
        }
    }
    connect()
}, false)