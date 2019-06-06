/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
TODO: test usage of flushexpiredtokens available through django's manage.py (see: 
  https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/

import tokenUtils from "./tokens.js"
import templateUtils from "./templates.js"

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
      var html = "<div>ERROR attempting to load login form.</div>";
      $( ".container" ).html( html );
    });
}

async function loadTemplate(access, refresh, template, retries){
  try {
    var content = await templateUtils.getTemplate(access, refresh, template, retries);
    var template = response.data;
    $( ".container" ).html( content );
  } catch (error) {
    loadLogin();
    $( ".errors" ).html( error );
  }
}

/*
check access and refresh to see if user is currently logged in
if so, load the home template
if not, load the login template
*/
function check_login(){
  try {
    var tokens = tokenUtils.getTokens();
  } catch (error) {
    console.log(error);
    loadLogin();
    return;
  }
  loadTemplate(tokens.access, tokens.refresh, 'template/index.html', 1);
}

check_login();


