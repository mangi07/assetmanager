/* **************************************************************
File: login.js

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
'use strict';

import tokenUtils from "./tokens.js"
import templateUtils from "./templates.js"

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function showError(message){
  var template = `<div>ERROR: ${message}</div>`;
  $( ".errors" ).html( message );
}

async function login(username, password) {
  try {
    await tokenUtils.requestTokens(username, password);
    var tokens = await tokenUtils.getTokens();
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
