document.addEventListener('DOMContentLoaded', () => {

    let socket = io();

    socket.on('connect', () => {
        socket.send('connected is correct');
    })

    socket.on('message', data => {
        // console.log(`Message received: ${data}`)
        const p = document.createElement('p');
        const br = document.createElement('br');
        p.innerHTML = data;
        document.querySelector('#display-message-section').append(p);

    });

    socket.on('some-event', data => {
        console.log(data);
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send(document.querySelector('#user_message').value);
    }

})