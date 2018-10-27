$(document).ready(function(){
    socket=io.connect(serverWebSocket+"/chat");
    // socket=io.connect("ws://45.32.45.1:80/chat", {transports: ['polling']});

    // build up websocket and join this room
    socket.on('connect', function(){
        socket.emit('join', {});
    });

    // listen messages
    socket.on('listen', function(message){
        console.log(message)
        $("<p />", {
            'class': 'message',
            'text': message['userName']+'(#'+message['userId']+'):'+
                    decodeURI(message['messageContent'])
        }).appendTo($('#chatBox'));
    });

    // listen users status
    socket.on('status', function(message){
        console.log(message)
        $("<p />", {
            'class': 'status',
            'text': message['userName']+'(#'+message['userId']+'):'+
                    message['content']
        }).appendTo($('#chatBox'));
    });

    // addEvents
    $("#submitBtn").click(function(){
        socket.emit("submit", {
            "content": encodeURI($("#textBox").val())
        });
    });

    $("#textBox").keydown(function(event){
        if (event.keyCode==13){
            $("#submitBtn").click();
            $("#textBox").val("");
        }
    });
});

function leaveRoom(){
    socket.emit('leave', {}, function(){
        socket.disconnect();
        
        window.location.href=serverUrl+"/index";
    });
}
