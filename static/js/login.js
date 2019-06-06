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

/*
function getHomeTemplate(access){
  //return axios({ method: 'post', url: 'http://localhost:8000/api/v1/template/index.html', headers: { Authorization: `Bearer ${access}` } })
  return requester.post('template/index.html', null, {
    headers: {'Authorization': 'Bearer ' + access}
  })
  .then(function (response) {
    //console.log("response received in getHomeTemplate on attempt to access temlate with token " + access);
    if (response.data === null || response.data === undefined){
      throw "Token used cannot access home.";
    }
    return response.data;
  });
}
*/

function showError(message){
  var template = `<div>ERROR: ${message}</div>`;
  $( ".errors" ).html( message );
}

//function sleep(ms) {
//  return new Promise(resolve => setTimeout(resolve, ms));
//}
async function login(username, password) {
  try {
    var debugtokens = await tokenUtils.requestTokens(username, password);
    //await sleep(300);
    var tokens = await tokenUtils.getTokens();
    console.log(debugtokens, tokens);
    var template = await templateUtils.getHomeTemplate(tokens.access);
  } catch (error) {
    showError(error);
  }
  $( ".container" ).html( template );
}

window.addEventListener("submit", function(event) {
  event.preventDefault();
  var user = $('#user').val();
  var pass = $('#pwd').val();;
  login(user, pass);
});
