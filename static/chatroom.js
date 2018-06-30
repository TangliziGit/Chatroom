GetMessagesInterval=1000

$(document).ready(function(){
    $("#submitBtn").click(function(){
        userName=$("#userName").text();

        $("#chatBox").append("<p>"+userName+": "+$("#textBox").val()+"</p>");
        $.post("/post", {
            "content": $("#textBox").val()
        }, function(data, status){});
    });

    $("#textBox").keydown(function(event){
        console.log(event);
        if (event.keyCode==13){
            $("#submitBtn").click();
            $("#textBox").val("");
        }
    });
});

function getMessages(recur){
    $.get('/get', function(data, status){
        items=jQuery.parseJSON(data);
        for (i in items){
            $("#chatBox").append("<p>"+ items[i]["user_name"] +"(#"+ items[i]["user_id"] +"): "+ items[i]["content"] +"</p>");
        }
    });

    if (recur){
        setTimeout(function(){getMessages(true)}, GetMessagesInterval);
    }
}


setTimeout(function(){getMessages(true)}, GetMessagesInterval)
