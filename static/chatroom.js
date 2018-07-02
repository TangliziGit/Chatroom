$(document).ready(function(){
    socketio=io.connect("ws://localhost:5000/chat", {transports: ['polling']});

    socketio.emit('connect', {});

    socketio.on('room_info', function(info){
        userId=     info['user_id'];
        userName=   info['user_name'];
        ifenter=    info['ifenter'];

        if (ifenter){
            $("#chatBox").append("<p id='enter'>"+userName+"(#"+userId+") Entered</p>");
        }else{
            $("#chatBox").append("<p id='leave'>"+userName+"(#"+userId+") Entered</p>");
        }
    });
    
    socketio.on('message', function(msg){
        userId=     msg['user_id'];
        userName=   msg['user_name'];
        content=    msg['content']

        $("#chatBox").append("<p id='content'>"+userName+"(#"+userId+"): "+content+"</p>");
    });

    // addEvents
    $("#submitBtn").click(function(){
        socketio.emit("submit", {"content": $("#textBox").val()});
    });

    $("#textBox").keydown(function(event){
        console.log(event);
        if (event.keyCode==13){
            $("#submitBtn").click();
            $("#textBox").val("");
        }
    });
});
