//fetch using a Request and a Headers objects
//using jsonplaceholder for the data

const uri = 'http://127.0.0.1:5000/api/?r=';

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
// function loadDoc(){
// fetch(req)
//     .then( (response)=>{
//         if(response.ok){
//             return response.json();
//         }else{
//             throw new Error('BAD HTTP stuff');
//         }
//     })
//     .then( (jsonData) =>{
//         console.log(jsonData);
//     })
//     .catch( (err) =>{
//         console.log('ERROR:', err.message);
//     });
// }
function loadDoc(){
    var uri_prepare = uri
    var inp = document.getElementById("input").value;
    uri_prepare += inp
    

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("content").innerHTML =this.responseText;
        var myArr = JSON.parse(this.responseText);
        console.log(myArr)
      }
    };
    xhttp.open("GET", uri_prepare, true);
    xhttp.send();
}