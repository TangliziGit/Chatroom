$(document).ready(function(){
    socketio=io.connect("ws://localhost:80/chat", {transports: ['polling']});
    // socketio=io.connect("ws://45.32.45.1:80/chat", {transports: ['polling']});

    socketio.emit('connect', {});

    socketio.on('room_info', function(info){
        userId=     info['user_id'];
        userName=   info['user_name'];
        ifenter=    info['ifenter'];

        if (ifenter){
            $("#chatBox").append("<p class='enter'>"+userName+"(#"+userId+") Entered</p>");
        }else{
            $("#chatBox").append("<p class='leave'>"+userName+"(#"+userId+") Entered</p>");
        }
    });
    
    socketio.on('message', function(msg){
        userId=     msg['user_id'];
        userName=   msg['user_name'];
        content=    msg['content'];

        console.log(msg);

        $("#chatBox").append("<p class='content'>"+userName+"(#"+userId+"): "+content+"</p>");
    });

    // addEvents
    $("#submitBtn").click(function(){
        socketio.emit("submit", {"content": encodeURIComponent($("#textBox").val())});
    });

    $("#textBox").keydown(function(event){
        if (event.keyCode==13){
            $("#submitBtn").click();
            $("#textBox").val("");
        }
    });
});
