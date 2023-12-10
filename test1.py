import requests
import json

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',

}
data = {
'call_id' : "9acfa117-101d-4ea5-850a-380894655b31",
'callback_url' : "http://172.104.247.154:8080/makecall/960684105/Leslie"
}
response = requests.post(
    'https://api.apivalley.su/api/v1/calls/transfer-call',
    headers=headers,
    json=data,  
    auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
)
print(response.text)