GetMessagesInterval=1000

lastDate=new Date();

$(document).ready(function(){
    $("#getMsgBtn").hide();
    $("#getMsgBtn").click(function(){getMessages(false)});

    $("#submitBtn").click(function(){
        lastDate=new Date();
        userName=$("#userNameBox").val();

        $("#chatBox").append("<p>"+userName+": "+$("#textBox").val()+"</p>");
        $.post("/post", {
            "time":lastDate.getTime(),
            "user":userName,
            "content": $("#textBox").val()
        }, function(data, status){
            // alert("Data: "+data+"\nStatus:"+status)
        });
    });
});

function getMessages(recur){
    userName=$("#userNameBox").val();
    getUrl="/get?time="+encodeURIComponent(lastDate.getTime())+
           "&user="+encodeURIComponent(userName);
    
    lastDate=new Date();
    $.get(getUrl, function(data, status){
        items=jQuery.parseJSON(data);
        for (i in items){
            $("#chatBox").append("<p>"+items[i]["user"]+": "+items[i]["content"]+"</p>");
        }
    });

    if (recur){
        setTimeout(function(){getMessages(true)}, GetMessagesInterval);
    }
}


setTimeout(function(){getMessages(true)}, GetMessagesInterval)
