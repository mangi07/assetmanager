/* ************************************************************** 
File: templates.js
* **************************************************************/
'use strict';

import tokenUtils from "./tokens.js"

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});


// should simply return a template
function getHomeTemplate(access){
	//return axios({ method: 'post', url: 'http://localhost:8000/api/v1/template/index.html', headers: { Authorization: `Bearer ${access}` } })
	return requester.post('template/index.html', null, {
	  headers: {'Authorization': 'Bearer ' + access}
	})
	.then(function (response) {
		if (response.data === null || response.data === undefined){
		  throw "Token used cannot access home.";
		}
		return response.data;
	});
}

function getTemplate(access, refresh, template, retries){
  return requester.post(template, null, {
    headers: {'Authorization': `Bearer ${access}`},
  })
    .then(function (response) {
      var template = response.data;
      return template;
    })
    .catch(async function (error) {
      // try to get new access and refresh based on the now assumed-to-be-expired access token
      if (retries <= 0) {
        throw "Cannot get template from server."
      } else {
        retries--;
      }
      await tokenUtils.renewTokens(refresh);
      var tokens = tokenUtils.getTokens();
      
      return getTemplate(tokens.access, tokens.refresh, template, retries);
    });
}

export default {
	getHomeTemplate,
	getTemplate,
}
