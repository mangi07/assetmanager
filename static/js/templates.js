import tokenUtils from "./tokens.js"

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});


// should simply return a template
function getHomeTemplate(access){
	return axios({ method: 'post', url: 'http://localhost:8000/api/v1/template/index.html', headers: { Authorization: `Bearer ${access}` } })
	//return requester.post('template/index.html', null, {
	//  headers: {'Authorization': 'Bearer ' + access}
	//})
	.then(function (response) {
		if (response.data === null || response.data === undefined){
		  throw "Token used cannot access home.";
		}
		return response.data;
		});
}

function getTemplate(access, refresh, template, retries){
  console.log("got inside getTemplate");
  return requester.post(template, {
    headers: {'Authorization': `Bearer ${access}`},
  })
    .then(function (response) {
      console.log("inside then"); // debug
      var template = response.data;
      return template;
    })
    .catch(async function (error) {
      console.log("inside catch"); // debug
      // TODO: try to get new access and refresh based on the now assumed-to-be-expired access token
      if (retries <= 0) {
        throw "Cannot get template from server."
      } else {
        retries--;
      }
      await tokenUtils.renewTokens(refresh); // test: is this guaranteed synchronous?
      var tokens = tokenUtils.getTokens();
      getTemplate(tokens.access, tokens.refresh, template, retries);
    });
}

export default {
	getHomeTemplate,
	getTemplate,
}