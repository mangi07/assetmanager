/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
TODO: test usage of flushexpiredtokens (see: 
  https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)
* **************************************************************/
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function testGetAssets(token){

}

function login(username, password){
  var data = {"username": username, "password": password};
  requester.post('/token/', data)
    .then(function (response) {
      // TODO: handle any users currently logged in on this machine 
      //   by logging out current user: delete tokens on machine (and optionally blacklist them immediately on server once blacklisting works)

      // handle success
      token = response;
      console.log(token);

      // TODO: save token on user's device
      
      // testing what token can access, then once done testing, redirect to home page

    })
    .catch(function (error) {
      // TODO: handle error, bad request here - show error on current page (login page)
      console.log(error);
    })
    .then(function (response) {
      // TODO: always executed (needed?)
    });

}

window.addEventListener("submit", function(event) {
  event.preventDefault();
  var user = $('#user').val();
  var pass = $('#pwd').val();;
  login(user, pass);
});
