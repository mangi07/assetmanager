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
		return null;
	}
	var access = tokens.access;
    var refresh = tokens.refresh;
    return {'access': access, 'refresh': refresh};
}

// TODO: refactor out the saving tokens part - similar code in login.js
function renewTokens(refresh) {
  var data = {'refresh': refresh};
  requester.post('token/refresh/', data)
    .then(function (response) {
      // handle success
      var accessToken = response.data.access;
      var refreshToken = response.data.refresh;
      
      setTokens(accessToken, refreshToken);
    });
    // TODO: handle error where tokens don't refresh??
}

export default {
	setTokens,
	getTokens,
	renewTokens,
}
