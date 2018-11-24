$(document).ready(function(){
    socket=io.connect(serverWebSocket+"/chat");

    // build up websocket and join this room
    socket.on('connect', function(){
        socket.emit('join', {});
    });

    // listen messages
    socket.on('listen', function(message){
        console.log(message);
        $("<div />", {
            'class': 'message'
        }).appendTo($('#chatBox'));
        $("<span />", {
            'class': 'message-user',
            'text': '■'+message['userName']+'(#'+message['userId']+'): ',
            'style': "color: "+message['userColorCode']
        }).appendTo($('.message:last'));
        $("<span />", {
            'class': 'message-content',
            'text': decodeURI(message['messageContent'])
        }).appendTo($('.message:last'));
    });

    // listen users status
    socket.on('status', function(message){
        console.log(message);
        $("<div />", {
            'class': 'message'
        }).appendTo($('#chatBox'));
        $("<span />", {
            'class': 'message-user',
            'text': '■'+message['userName']+'(#'+message['userId']+'): ',
            'style': "color: "+message['userColorCode']
        }).appendTo($('.message:last'));
        $("<u />", {
            'class': 'message-status',
            'text': decodeURI(message['messageContent'])
        }).appendTo($('.message:last'));
    });

    // addEvents
    $("#submitBtn").click(function(){
        socket.emit("submit", {
            "content": encodeURI($("#textBox").val())
        });
        $("#textBox").val("");
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
