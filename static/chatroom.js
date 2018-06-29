GetMessagesInterval=1000

$(document).ready(function(){
    // $("#getMsgBtn").hide();
    // $("#getMsgBtn").click(function(){getMessages(false)});

    $("#submitBtn").click(function(){
        userName=$("#userName").text();

        $("#chatBox").append("<p>"+userName+": "+$("#textBox").val()+"</p>");
        $.post("/post", {
            "content": $("#textBox").val()
        }, function(data, status){
            // alert("Data: "+data+"\nStatus:"+status)
        });
    });
});

function getMessages(recur){
    $.get('/get', function(data, status){
        items=jQuery.parseJSON(data);
        console.log(items)
        for (i in items){
            $("#chatBox").append("<p>"+ items[i]["user_name"] +"(#"+ items[i]["user_id"] +"): "+ items[i]["content"] +"</p>");
        }
    });

    if (recur){
        setTimeout(function(){getMessages(true)}, GetMessagesInterval);
    }
}


setTimeout(function(){getMessages(true)}, GetMessagesInterval)
