import requests

BASE_URL = "http://192.168.1.1"
LOGIN_URL = "http://192.168.1.1/rest/v1/user/login"
BAND2G_CONFIG_URL = "http://192.168.1.1/rest/v1/wifi/band2g/config"
BAND5G_CONFIG_URL = "http://192.168.1.1/rest/v1/wifi/band5g/config"
BAND2G_STATE_URL = "http://192.168.1.1/rest/v1/wifi/band2g/state"
BAND5G_STATE_URL = "http://192.168.1.1/rest/v1/wifi/band5g/state"

session = requests.Session()

def print_error(response):
    try: 
        data = response.json()
        print("ErrorCode:\t" , data.get("errorCode"))
        print("Message:\t" , data.get("message"))
    except:
        print("No json data")

def login(password):
    response = session.post(LOGIN_URL, json={"password": password})
    data = response.json()
    token = ""
    if response.status_code == 401:
        print("Login Failed")
        print_error(response)

    elif response.status_code == 201: 
        print("Login Successful")
        token = data.get('created').get('token')
        return token
    else:
        print("There was an internal error:\n")
        print_error(response)
    return None

def get_header(token):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Authorization": f'Bearer {token}',
            "Content-Type": "application/json"
        }
def turn_on_wifi(header):
    json_2g= {
        "config":{
            "enable":True,
            "radio":{"mode":"g_n_ax"}
        }
    }

    json_5g= {
        "config":{
            "enable":True,
            "radio":{"mode":"a_n_ac_ax"}
        }
    }
    response_2g = session.patch(BAND2G_CONFIG_URL, json=json_2g, headers=header)
    response_5g = session.patch(BAND5G_CONFIG_URL, json=json_5g, headers=header)

    if response_2g.ok and response_5g.ok:
        print("Turned on wifi!")
    else:
        print("Failed to turn on wifi")
        print_error(response_2g)
        print_error(response_5g)
    return response_2g, response_5g

def turn_off_wifi(header):
    json = {
        "config":{
            "enable":False,
            "radio":{} 
            } 
        }
    response_2g = session.patch(BAND2G_CONFIG_URL, json=json, headers=header)
    response_5g = session.patch(BAND5G_CONFIG_URL, json=json, headers=header)
    if response_2g.ok and response_5g.ok:
        print("Turned off wifi!")
    else: 
        print("Failed to turn off wifi")
        print_error(response_2g)
        print_error(response_5g)
    return response_2g, response_5g

def get_state(header, band='5g') -> Boolean:
    if band == '5g':
        response_5g = session.get(BAND5G_STATE_URL, headers=header)
        if response_5g.ok:
            band5g_state = response_5g.json().get("state").get("enable")
            if band5g_state: 
                print("Wifi (5g) currently on")
            else: 
                print("Wifi (5g) is currently off")
            return band5g_state 
        else:
            print_error(response_5g)
            raise Exception("Failed to 5g get status")
    elif '2g': 
        response_2g = session.get(BAND2G_STATE_URL, headers=header)
        if response_2g.ok:
            band2g_state = response_2g.json().get("state").get("enable")
            if band2g_state: 
                print("Wifi (2g) is currently off")
            else:
                print("Wifi (2g) is currently off")
            return band2g_state
        else:
            print_error(response_2g)
            raise Exception("Failed to get 2g status")
    else:
        raise Exception("invalid band")

def toggle_wifi(header):
    band5g_state = get_state(header, '5g')
    band2g_state = get_state(header, '2g')
    if band2g_state or band5g_state:
        response_2g, response_5g = turn_off_wifi(header)
        return response_2g, response_5g
    else:
        response_2g, response_5g = turn_on_wifi(header)
        return response_2g, response_5g


def logout(token):
    DELETE_URL =  BASE_URL + f'/rest/v1/user/3/token/{token}'
    header = get_header(token)
    response = session.delete(DELETE_URL, headers=header)
    if response.ok: 
        print("Logout Successful")
    else: 
        print("Logout Failed")
    return response
