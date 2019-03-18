//import {axios} from './axios.min.js'

/* ************************************************************** 
JWT TOKEN AUTHENTICATION USAGE
https://github.com/davesque/django-rest-framework-simplejwt#usage
* **************************************************************/


/*

// Make a request for a user with a given ID
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
  auth: {
    username: 'admin',
    password: 'password'
  },
});


requester.get('/assets')
  .then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });

*/

const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
});

  
var data = {"username": "admin", "password": "password"};
requester.post('/token/', data)
  .then(function (response) {
    // handle success
    console.log(response);
    // save token on user's device
    
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });
