import requests

base_url = 'http://localhost:8000/'

# ###################################################################################################
# superuser must already be created with username 'admin' and password 'password'
# TEST superadmin can access all urls
result = requests.post(base_url + 'api/v1/token/', data={"username":"admin", "password": "password"})
superuser_token = result.json()['access']

result = requests.get(base_url + 'home/', 
	headers={'Authorization': 'Bearer {}'.format(superuser_token)}
)
assert result.status_code == 200

# TODO: create and test manager and regular user

def test_response(url, token, expected_status_code):
	result = requests.post(base_url + url,
	    headers={'Authorization': 'Bearer {}'.format(token)}
	)
	print('status: ' + str(result.status_code))
	assert result.status_code == expected_status_code

api_version = 'api/v1/'
tests = [
	#(api_version, 1, 1, 1), 
	#(api_version + 'assets/', 1, 1, 1), 
	#(api_version + 'bulkDelete/', 1, 1, 1), 
	#(api_version + 'assets/1/', 1, 1, 1), 
	#(api_version + 'locations/', 1, 1, 1), 
	#(api_version + 'locations/bulkDelete', 1, 1, 1), 
	(api_version + 'user/create/', 400, 1, 1), 
	('home/', 200, 1, 1), 
	# TODO: login/
	# TODO: about/
	# TODO??: token/refresh/
]

for url, superuser_status, manager_status, regular_user_status in tests:
	print("Testing url: " + url)

	print("Expected status when user is allowed to access url: " + str(superuser_status))
	test_response(url, superuser_token, superuser_status)

	print("Expected status when user is not allowed to access url: 403")
	test_response(url, None, 403)

	print("Passed.\n")

