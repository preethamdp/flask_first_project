//fetch using a Request and a Headers objects
//using jsonplaceholder for the data

const uri = 'http://127.0.0.1:5000/api/?r=';
var head = document.getElementsByTagName("head")[0]
var len_json_data;
//new Request(uri)
//new Request(uri, options)
//options - method, headers, body, mode
//methods:  GET, POST, PUT, DELETE, OPTIONS

//new Headers()
// headers.append(name, value)
// Content-Type, Content-Length, Accept, Accept-Language,
// X-Requested-With, User-Agent
let h = new Headers();
h.append('Accept', 'application/json');

let req = new Request(uri, {
    method: 'GET',
    headers: h,
    mode: 'cors'
});
function enterKey(){
  var input = document.getElementById("bot-input-value");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("bot-send").click();
  }
});
}
function loadDoc(){
    enterKey()
    var uri_prepare = uri
    var inp = document.getElementById("bot-input-value").value;
    document.getElementById("bot-input-value").value = null
    if (inp!=""){
    //user message
    var user_data = document.createElement("script");
          user_data.setAttribute('type','text/javascript');
          user_data.innerHTML = "botui.message.add({human:true,\ncontent: '"+inp.toString()+"'});"
          head.appendChild(user_data)

    uri_prepare += inp
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        console.log(len = Object.keys(myArr).length);
        console.log(myArr)
        console.log(len)
        
        for(var key in myArr){
          len_data = Object.keys(myArr[key]).length;
          console.log(len_data)
          break;
        }
        for(var key in myArr){
          var single_data = document.createElement("script");
          single_data.setAttribute('type','text/javascript');
          if(len_data==2){
          //single_data.innerHTML = "botui.message.add({content: '"+key.toString()+"'});"
          single_data.innerHTML = "botui.message.add({content: '"+key.toString()
          single_data.innerHTML += ": "+myArr[key][1]+" [visit site]("+myArr[key][0].toString()+")^'});"
          head.appendChild(single_data); 
        }
          else if(len==1){
            single_data.innerHTML = "botui.message.add({content: '"+myArr[key].toString()+"'});"
            head.appendChild(single_data);
          }
          
        }

      }
    
    };
    xhttp.open("GET", uri_prepare, true);
    xhttp.send();
  }

}
