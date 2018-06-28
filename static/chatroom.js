lastDate=new Date();

$(document).ready(function(){
    $("#submitBtn").click(function(){
        lastDate=new Date();
        userName=$("#userNameBox").val();

        $("div").append("<p>"+userName+": "+$("#textBox").val()+"</p>");
        $.post("/post", {
            "time":lastDate.getTime(),
            "user":userName,
            "content": $("#textBox").val()
        }, function(data, status){
            // alert("Data: "+data+"\nStatus:"+status)
        });
    });

    $("#getMsgBtn").click(function(){
        userName=$("#userNameBox").val();

        getUrl="/get?time="+encodeURIComponent(lastDate.getTime())+
            "&user="+encodeURIComponent(userName);
        
        lastDate=new Date();
        $.get(getUrl, function(data, status){
            // alert(data+"\n"+status);
            items=jQuery.parseJSON(data);
            // alert(items);
            for (i in items){
                $("div").append("<p>"+items[i]["user"]+": "+items[i]["content"]+"</p>");
            }
        });
    })
});
