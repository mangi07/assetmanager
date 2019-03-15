//import {axios} from './axios.min.js'

// Make a request for a user with a given ID
const requester = axios.create({
  baseURL: '/api/v1/',
  //timeout: 1000,
  auth: {
    username: 'admin',
    password: 'password'
  },
});

var res = {};

requester.get('/assets')
  .then(function (response) {
    // handle success
    console.log(response);
    console.log(res);
    res.data = response;
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });