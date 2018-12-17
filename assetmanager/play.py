import requests

#r = requests.delete('http://localhost:8000/api/vi/locations', auth=('admin', 'password'), json=[6])


#r = requests.get('http://localhost:8000/api/vi/locations?id=18', auth=('admin', 'password'))

#q = requests.get('http://localhost:8000/api/v1/locations?description_like=www', auth=('admin', 'password'))


#q = requests.get('http://localhost:8000/api/v1/locations', auth=('admin', 'password'))

#q = requests.delete('http://localhost:8000/api/v1/locations', auth=('admin', 'password'), json=[34])

q = requests.delete('http://localhost:8000/api/v1/assets', auth=('admin', 'password'), json=[24])

print(q.text)