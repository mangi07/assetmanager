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


function login(username, password){
  var data = {"username": username, "password": password};
  requester.post('/token/', data)
    .then(function (response) {
      // TODO: handle any users currently logged in on this machine 
      //   by logging out current user: delete tokens on machine (and optionally blacklist them immediately on server once blacklisting works)

      // handle success
      accessToken = response.data.access;
      refreshToken = response.data.refresh;
      tokenData = {'access': accessToken, 'refresh': refreshToken};

      // TODO: save token on user's device
      window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
      
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
