/* **************************************************************
File: tokens.js

Description: utlitity functions to manage api tokens

Documentation: https://github.com/davesque/django-rest-framework-simplejwt
  JWT TOKEN AUTHENTICATION USAGE
  https://github.com/davesque/django-rest-framework-simplejwt#usage
  
  TODO: test usage of flushexpiredtokens available through django's manage.py
  (see: https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)
************************************************************** */
'use strict';

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function setTokens(access, refresh) {
  if (access===undefined) {
    throw "In setTokens, access undefined.";
  } else if (refresh===undefined) {
    throw "In setTokens, refresh undefined.";
  }
	var tokenData = {'access': access, 'refresh': refresh};
  // save token on user's device
  window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
}

function getTokens() {
	var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
	if (tokens === null) {
		throw "Cannot obtain requested tokens from user's device."
	}
	var access = tokens.access;
  var refresh = tokens.refresh;
  return {'access': access, 'refresh': refresh};
}

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
  console.log("refresh requested");
  var data = {'refresh': refresh};
  return requester.post('token/refresh/', data)
    .then(function (response) {
      // handle success
      var accessToken = response.data.access;
      var refreshToken = response.data.refresh;
      
      setTokens(accessToken, refreshToken);
      console.log("This should come before template requested in inner getTemplate");
    });
}

export default {
	setTokens,
	getTokens,
	requestTokens,
	renewTokens,
}
