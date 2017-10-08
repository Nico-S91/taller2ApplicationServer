from http import client
import urllib
import json

conn = client.HTTPConnection("stormy-lowlands-30400.herokuapp.com")
url = '/api/v1/users/validate?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImxsZXZhbWUiLCJpYXQiOjE1MDczODkxODQsImV4cCI6MTUwOTk4MTE4NH0.KGdbsCbiYQMXXhtuogpKX6FslNTRIg9wVadI_F-w5Ko'
body = {"username": "mzaragoza", "password": "pepe"}

conn.request('POST', url, json.dumps(body), {'Content-Type':'application/json'})
res = conn.getresponse()
print(res.status, res.reason, res.readlines())
