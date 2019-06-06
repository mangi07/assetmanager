import requests

#r = requests.delete('http://localhost:8000/api/vi/locations', auth=('admin', 'password'), json=[6])


#r = requests.get('http://localhost:8000/api/vi/locations?id=18', auth=('admin', 'password'))

#q = requests.get('http://localhost:8000/api/v1/locations?description_like=www', auth=('admin', 'password'))


#q = requests.get('http://localhost:8000/api/v1/locations', auth=('admin', 'password'))

#q = requests.delete('http://localhost:8000/api/v1/locations', auth=('admin', 'password'), json=[34])

#q = requests.delete('http://localhost:8000/api/v1/assets', auth=('admin', 'password'), json=[24])

#print(q.text)


#result = requests.post('http://localhost:8000/api/v1/token/', data={"username":"admin", "password": "password"})
#token = result.json()['access']
#result = requests.post('http://localhost:8000/api/v1/user/create/',
#    headers={'Authorization': 'Bearer {}'.format(token)},
#    data={"username": "manager user 2", "password": "123", "confirmPassword": "password",
#        "department": "AV", "user_type": "manager"}
#)
#
#print(result)
#print(result.text)

result = requests.post('http://localhost:8000/api/v1/token/', data={"username":"admin", "password": "password"})
token = result.json()['access']
print(token)
#token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTU5Nzc2NjA3LCJqdGkiOiIwZWIzMzFmMTdjOWU0OTQ5YjhhZmI2MGZiMTY1MTEzZSIsInVzZXJfaWQiOjEyfQ.oPs00QYBRR7OcLZjytdZlzuIkAH7zse4AdxkT7uouZE"
#token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTU5Nzg0OTEwLCJqdGkiOiI0MzdkOTIxMzVjMDQ0NzY5OWM5Mjc3MTlkMTBlZmI1OSIsInVzZXJfaWQiOjEyfQ.5MNplhpobwP8kZHjitUzcF_0ak_zxns0YmGs7qE_8c0"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTU5Nzg0OTk5LCJqdGkiOiJjYzQ3MGJlYzE3Njk0OWYyODBjYzYxY2ExZDMxZDA3NiIsInVzZXJfaWQiOjEyfQ.xTRhti1GCUz1Bun74ecAa56EjFlnOioPDiYso0cc0DQ"
result = requests.post('http://localhost:8000/api/v1/template/index.html/',
    headers={'Authorization': 'Bearer {}'.format(token)},
)
#result = requests.post('http://localhost:8000/api/v1/template/index.html/')
print(result)
print(result.text)