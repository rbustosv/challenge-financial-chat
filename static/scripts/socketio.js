document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    const username = document.querySelector('#get-username').innerHTML;

    let room = "general";
    joinRoom("general");

    socket.on('connect', () => {
        socket.send('I am connected!');
    });

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        p.innerHTML = data;
        if (data.username) {
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg);
        }
        
    });


    //sending message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg':document.querySelector('#user_message').value,
        'username':username, 'room': room });
        //cleaning input area
        document.querySelector('#user_message').value='';
    }

    //room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;

            }
        };
    });

    //leaving room
    function leaveRoom(room) {
        socket.emit('leave',{'username': username, 'room': room});
    }

    //joining room
    function joinRoom(room){
        socket.emit('join',{'username': username, 'room': room});
        //cleaning message area
        document.querySelector('#display-message-section').innerHTML='';
        document.querySelector('#user_message').focus();
    }

    // printing system message
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})