import json
import requests

url = 'https://stormy-lowlands-30400.herokuapp.com/api/v1/users/validate?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImxsZXZhbWUiLCJpYXQiOjE1MDczODkxODQsImV4cCI6MTUwOTk4MTE4NH0.KGdbsCbiYQMXXhtuogpKX6FslNTRIg9wVadI_F-w5Ko'
response = requests.post(url,json={'username':'mzaragoza','password':'pepe'})
json_data = json.loads(response.text)

print(json_data)
print(response.status_code)
