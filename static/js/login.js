/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
* **************************************************************/
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function login(username, password){
  //var data = {"username": "admin", "password": "password"};
  var data = {"username": username, "password": password};
  requester.post('/token/', data)
    .then(function (response) {
      // TODO: handle bad request

      // handle success
      token = response;
      console.log(token);

      // TODO: save token on user's device
      
    })
    .catch(function (error) {
      // TODO: handle error
      console.log(error);
    })
    .then(function (response) {
      // TODO: always executed (needed?)
    });

}

var loginForm = document.getElementById("login");
var token;
window.addEventListener("submit", function(event) {
  event.preventDefault();
  var user = $('#user').val();
  var pass = $('#pwd').val();;
  login(user, pass);
});
