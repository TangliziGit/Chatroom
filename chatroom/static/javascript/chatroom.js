window.onbeforeunload=function () {
    socketio.emit('disconnect', {});
};

$(document).ready(function(){
    socketio=io.connect("ws://localhost:80/chatroom");
    // socketio=io.connect("ws://45.32.45.1:80/chat", {transports: ['polling']});

    socketio.emit('connect', {});

    socketio.on('message', function(message){
        $("<p />", {
            'class': 'messages',
            'text': message['userName']+'(#'+message['userId']+'):'+
                    message['content']
        }).appendTo($('#chatBox'))
    });

    // addEvents
    $("#submitBtn").click(function(){
        socketio.emit("submit", {
            "content": encodeURIComponent($("#textBox").val())
        });
    });

    $("#textBox").keydown(function(event){
        if (event.keyCode==13){
            $("#submitBtn").click();
            $("#textBox").val("");
        }
    });
});
