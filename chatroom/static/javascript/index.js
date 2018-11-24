function createRoomsList(roomlist){
    var roomsHolder="#rooms-holder";

    console.log(roomlist)
    for (var i in roomlist){
        var room="#room_"+i;
        // console.log(roomlist[i]);
        
        $("<tr />", {
            "id": "room_"+i,
            "class": "room"
        }).appendTo(roomsHolder);

        $("<td />", {
            "id": "room_"+i+"_id",
            "class": "room-id",
            "text": "#"+roomlist[i]['roomId']
        }).appendTo(room);
        $("<td />", {
            "id": "room_"+i+"_name",
            "class": "room-name"
            // "text": roomlist[i]['roomName']
        }).appendTo(room);
        $("<a />", {
            "class": "roomHref",
            "href": serverUrl+"/chat/chatroom?roomId="+roomlist[i]['roomId'],
            "text": roomlist[i]['roomName'],
        }).appendTo("#room_"+i+"_name");
        $("<td />", {
            "id": "room_"+i+"_creator",
            "class": "room-creator",
            "text": roomlist[i]['hostUserName']
        }).appendTo(room);
        $("<td />", {
            "id": "room_"+i+"_status",
            "class": "room-status",
            "text": roomlist[i]['userlist'].length+"/"+roomlist[i]['roomCapacity']
        }).appendTo(room);
    }
}

$(document).ready(function(){
    $.ajax({
        url: serverUrl+"/chat/roomlist",
        async: true,
        success: function(response){
            console.log(response);
            createRoomsList(JSON.parse(response));
        }
    })

    $.ajax({
        url: hitokotoUrl,
        async: true,
        success: function(response){
            $("#hitokoto").text('『'+response['hitokoto']+'』');
            $("#hitokoto-from").text('「'+response['from']+'」');
        }
    })
})
