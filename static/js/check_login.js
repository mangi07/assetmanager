/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
TODO: test usage of flushexpiredtokens available through django's manage.py (see: 
  https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});


function check_login(username, password){
  requester.post('/token/', data)
    .then(function (response) {
      // TODO: once done testing, redirect to home page
      access = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken')).access;
      refresh = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken')).refresh;
      window.location.href = '/home/';

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
