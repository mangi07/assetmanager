import requests

r = requests.delete('http://localhost:8000/api/vi/locations', auth=('admin', 'password'), json=[6])

print(r.text)