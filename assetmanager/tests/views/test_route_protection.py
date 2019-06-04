import requests
from enum import Enum
from collections import namedtuple

base_url = 'http://localhost:8000/'
class Method(Enum):
	GET = 1
	POST = 2

# ###################################################################################################
# superuser must already be created with username 'admin' and password 'password'
# get token for superuser
result = requests.post(base_url + 'api/v1/token/', data={"username":"admin", "password": "password"})
superuser_token = result.json()['access']
# ###################################################################################################
# create manager user and get manager user token
result = requests.post(base_url + 'api/v1/user/create/', 
	headers={'Authorization': 'Bearer {}'.format(superuser_token)},
	data={"username":"manager", "password": "password", "confirmPassword": "password",
		"department": "DEFAULT", "user_type": "manager"}
)
result = requests.post(base_url + 'api/v1/token/', data={"username":"manager", "password": "password"})
manager_token = result.json()['access']
# ###################################################################################################
# create regular user and get regular user token
result = requests.post(base_url + 'api/v1/user/create/', 
	headers={'Authorization': 'Bearer {}'.format(superuser_token)},
	data={"username":"regular", "password": "password", "confirmPassword": "password",
		"department": "DEFAULT", "user_type": "regular"}
)
result = requests.post(base_url + 'api/v1/token/', data={"username":"regular", "password": "password"})
user_token = result.json()['access']
# TODO: create and test manager and regular user


def test_response(url, method, token, expected_status_code, redirect=False):

	if method == Method.POST:
		result = requests.post(base_url + url,
		    headers={'Authorization': 'Bearer {}'.format(token)}
		)
	elif method == Method.GET:
		result = requests.get(base_url + url,
			headers={'Authorization': 'Bearer {}'.format(token)}
		)
	print()
	if redirect:
		redirect_status = result.history[0].status_code
		print('redirect status: ' + str(redirect_status))
		assert redirect_status == expected_status_code
	else:
		print('status: ' + str(result.status_code))
		assert result.status_code == expected_status_code


def test_user(url, method, token, expected_status, redirect):
	print('######################################################')
	print("Testing url: " + url)

	print("Expected status, attempting to access url: " + str(expected_status))
	test_response(url, method, token, expected_status, redirect)

	print("Passed.\n")


api_version = 'api/v1/'
# TODO: this may be sufficient, but it's more thorough to test access to each method for each route
UserTest = namedtuple('UserTest', ['url', 'method', 'token', 'expected_status', 'redirect'])
tests = [
	UserTest(api_version, Method.GET, superuser_token, 200, False), 
	UserTest(api_version, Method.GET, manager_token, 200, False), 
	UserTest(api_version, Method.GET, user_token, 200, False), 
	UserTest(api_version, Method.GET, None, 403, False), 

	UserTest(api_version + 'assets/', Method.GET, superuser_token, 200, False), 
	UserTest(api_version + 'assets/', Method.GET, manager_token, 200, False), 
	UserTest(api_version + 'assets/', Method.GET, user_token, 200, False), 
	UserTest(api_version + 'assets/', Method.GET, None, 403, False), 

	UserTest(api_version + 'assets/bulkDelete/', Method.POST, superuser_token, 400, False), 
	UserTest(api_version + 'assets/bulkDelete/', Method.POST, manager_token, 400, False), 
	UserTest(api_version + 'assets/bulkDelete/', Method.POST, user_token, 400, False), 
	UserTest(api_version + 'assets/bulkDelete/', Method.POST, None, 403, False),

	UserTest(api_version + 'assets/9999/', Method.GET, superuser_token, 404, False), # assuming db has no asset with asset_id 9999
	UserTest(api_version + 'assets/9999/', Method.GET, manager_token, 404, False), 
	UserTest(api_version + 'assets/9999/', Method.GET, user_token, 404, False), 
	UserTest(api_version + 'assets/9999/', Method.GET, None, 403, False),

	UserTest(api_version + 'locations/', Method.GET, superuser_token, 200, False), 
	UserTest(api_version + 'locations/', Method.GET, manager_token, 200, False), 
	UserTest(api_version + 'locations/', Method.GET, user_token, 200, False), 
	UserTest(api_version + 'locations/', Method.GET, None, 403, False), 

	UserTest(api_version + 'locations/bulkDelete/', Method.POST, superuser_token, 400, False), 
	UserTest(api_version + 'locations/bulkDelete/', Method.POST, manager_token, 400, False), 
	UserTest(api_version + 'locations/bulkDelete/', Method.POST, user_token, 400, False), 
	UserTest(api_version + 'locations/bulkDelete/', Method.POST, None, 403, False), 
	
	UserTest(api_version + 'user/create/', Method.POST, superuser_token, 400, False), 
	UserTest(api_version + 'user/create/', Method.POST, manager_token, 400, False), 
	UserTest(api_version + 'user/create/', Method.POST, user_token, 400, False), 
	UserTest(api_version + 'user/create/', Method.POST, None, 403, False),
	
	UserTest('home/', Method.GET, superuser_token, 200, False), 
	UserTest('home/', Method.GET, manager_token, 200, False), 
	UserTest('home/', Method.GET, user_token, 200, False), 
	UserTest('home/', Method.GET, None, 302, True),
	
	# TODO: login/
	# TODO: about/
	# TODO??: token/refresh/
]


for test in tests:
	test_user(test.url, test.method, test.token, test.expected_status, test.redirect)

# ###################################################################################################
# TODO: route user/delete does not exist yet
# TODO: delete test users manager and reqular user
# TODO: Cannot do it the following way because this script does not load django settings needed for User import to work
# Therefore, you need to create a route to delete users, test it, and then use it.
# For now, after running the test, you need to run these lines in python manage.py shell:
#   from django.contrib.auth.models import User
#   User.objects.get(username="manager").delete()
#   User.objects.get(username="regular").delete()

"""
result = requests.post(base_url + 'api/v1/user/delete/', 
	headers={'Authorization': 'Bearer {}'.format(superuser_token)},
	data={"username":"manager", "password": "password", "confirmPassword": "password",
		"department": "DEFAULT", "user_type": "manager"}
)
result = requests.post(base_url + 'api/v1/user/delete/', 
	headers={'Authorization': 'Bearer {}'.format(superuser_token)},
	data={"username":"manager", "password": "password", "confirmPassword": "password",
		"department": "DEFAULT", "user_type": "manager"}
)
"""