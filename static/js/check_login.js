/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
TODO: test usage of flushexpiredtokens available through django's manage.py (see: 
  https://github.com/davesque/django-rest-framework-simplejwt#blacklist-app)

Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

function loadTemplate(token, template){
  requester.post(template, {
    headers: {'Authorization': `Bearer ${token}`}
  })
    .then(function (response) {
      console.log(response);
      var template = response;
      $( ".container" ).html( template );
    })
    .catch(function (error) {
      // TODO: handle error, bad request here - show error on current page (login page)
      console.log(error);
      // TODO: work with axios to conditionally set authorization header when needed, before making request
      loadTemplate(null, 'template/login');
    })
    .then(function (response) {
      // TODO: always executed (needed?)
    });
}

/*
check access and refresh to see if user is currently logged in
if so, load the home template
if not, load the login template
*/
function check_login(){
  token = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));

  if (token === null) {
    // TODO: load home template into base.html's container
    loadTemplate(null, 'template/login');
  } else {
    access = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken')).access;
    // TODO: need a way to check and get new access and refresh
    refresh = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken')).refresh;
    // TODO: load login template into base.html's container
    loadProtectedTemplate(access, 'template/index/');
  }

}

check_login();