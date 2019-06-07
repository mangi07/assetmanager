/* ************************************************************** 
File: check_login.js

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
'use strict';

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
    console.log("content to be loaded into container:");
    console.log(content);
    $( ".container" ).html( content );
  } catch (error) {
    console.log(error);
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


