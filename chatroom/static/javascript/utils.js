function toDate(timestamp){
    var date =  new Date(obj);
    var year = 1900+date.getYear();
    var mon = "0"+(date.getMonth()+1);
    var day = "0"+date.getDate();
    return year+"-"+mon.substring(m.length-2,m.length)+"-"+day.substring(d.length-2,d.length);
}

var serverUrl="http://localhost";
var serverWebSocket="ws://localhost";
var hitokotoUrl="https://v1.hitokoto.cn/?c=a";
