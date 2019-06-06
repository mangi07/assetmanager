/*
File: tokens.js
Description: utlitity functions to manage api tokens
*/

'use strict';

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function setTokens(access, refresh) {
	var tokenData = {'access': access, 'refresh': refresh};
    // save token on user's device
    window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
}

function getTokens() {
	var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
	if (tokens === null) {
    console.log("Tokens: " + tokens);
		throw "Cannot obtain requested tokens from user's device."
	}
	var access = tokens.access;
  var refresh = tokens.refresh;
  return {'access': access, 'refresh': refresh};
}

/*
function getHomeTemplate(access){
  //return axios({ method: 'post', url: 'http://localhost:8000/api/v1/template/index.html', headers: { Authorization: `Bearer ${access}` } })
  return requester.post('template/index.html', null, {
    headers: {'Authorization': 'Bearer ' + access}
  })
  .then(function (response) {
    //console.log("response received in getHomeTemplate on attempt to access temlate with token " + access);
    if (response.data === null || response.data === undefined){
      throw "Attempt to access home failed with token used.";
    }
    return response.data;
  });
}
*/
function requestTokens(username, password) {
	var data = {"username": username, "password": password};
	return requester.post('/token/', data)
    .then(function (response) {
	    // Note: user may have tokens saved in local storage or session storage overwritten here.

	    // handle success
	    var accessToken = response.data.access;
	    var refreshToken = response.data.refresh;

	    // save token on user's device
	    setTokens(accessToken, refreshToken); // assumed to be synchronous!!

	    return {'access': accessToken, 'refresh': refreshToken};
	  });
}

function renewTokens(refresh) {
  var data = {'refresh': refresh};
  return requester.post('token/refresh/', data)
    .then(function (response) {
      // handle success
      var accessToken = response.data.access;
      var refreshToken = response.data.refresh;
      
      setTokens(accessToken, refreshToken);
    });
}

export default {
	setTokens,
	getTokens,
	requestTokens,
	renewTokens,
}
