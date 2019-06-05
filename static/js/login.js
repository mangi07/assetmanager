/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
TODO: test usage of flushexpiredtokens available through django's manage.py (see: 
  https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/

import tokenUtils from "./tokens.js"

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function getHomeTemplate(access){
  return requester.post('/template/index.html',  {
    headers: {'Authorization': `Bearer ${access}`}
  })
    .then(function (response) {
      return response.data;
    })
    .catch(function (error) {
      // TODO: do something here
      console.log("error from getHomeTemplate: " + error)
    });
}

// TODO: refactor out the saving tokens part - similar code in check_login.js
function login(username, password){
  var data = {"username": username, "password": password};
  requester.post('/token/', data)
    .then(function (response) {
      // Note: user may have old tokens saved in local storage or session storage.

      // handle success
      var accessToken = response.data.access;
      var refreshToken = response.data.refresh;
      //var tokenData = {'access': accessToken, 'refresh': refreshToken};

      // save token on user's device
      //window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
      tokenUtils.setTokens(accessToken, refreshToken);

      var tokens = tokenUtils.getTokens();

      // load home page content
      var template = "<div>ERROR</div>";
      getHomeTemplate(tokens.access).then(
        function (result) {
          if (result === null || result === undefined){
            throw "New tokens obtained but cannot access home.";
          }
          var template = result;
          console.log(template);
          $( ".errors" ).html( template );
        }
      )
        .catch(function (error) { 
          console.log(error);
          var template = `<div>ERROR: ${error}</div>`;
          $( ".errors" ).html( template );
        });

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
