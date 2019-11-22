document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        //13 = enterkey
        if (event.keycode === 13){
            document.querySelector('#send_message').click();
        }
    })
})