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

function loadLogin(){
  var template = '/login/';
  requester.get(template)
    .then(function (response) {
      var template = response.data;
      $( ".container" ).html( template );
    })
    .catch(function (error) {
      console.log(error);
      var html = "<div>ERROR</div>";
      $( ".container" ).html( html );
    });
}

function loadTemplate(access, refresh, template, retries){
  requester.post(template, {
    headers: {'Authorization': `Bearer ${access}`},
  })
    .then(function (response) {
      var template = response.data;
      $( ".container" ).html( template );
    })
    .catch(function (error) {
      console.log(error);
      // TODO: try to get new access and refresh based on the now assumed-to-be-expired access token
      if (retries <= 0) {
        loadLogin();
        return;
      } else {
        retries--;
      }
      try {
        tokenUtils.renewTokens(refresh);
        var tokens = tokenUtils.getTokens();
        loadTemplate(tokens.access, tokens.refresh, template, retries);
      } catch {
        loadLogin();
      }
    });
}

/*
check access and refresh to see if user is currently logged in
if so, load the home template
if not, load the login template
*/
function check_login(){
  var tokens = tokenUtils.getTokens();
  if (tokens === null) {
    loadLogin();
  } else {
    console.log(tokens);
    loadTemplate(tokens.access, tokens.refresh, 'template/index.html', 1);
  }

}

check_login();


