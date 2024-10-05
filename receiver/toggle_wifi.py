import requests

BASE_URL = "http://192.168.1.1"
LOGIN_URL = "http://192.168.1.1/rest/v1/user/login"
BAND2G_CONFIG_URL = "http://192.168.1.1/rest/v1/wifi/band2g/config"
BAND5G_CONFIG_URL = "http://192.168.1.1/rest/v1/wifi/band5g/config"
BAND2G_STATE_URL = "http://192.168.1.1/rest/v1/wifi/band2g/state"
BAND5G_STATE_URL = "http://192.168.1.1/rest/v1/wifi/band5g/state"

session = requests.Session()

def login(password):
    response = session.post(LOGIN_URL, json={"password": password})
    data = response.json()
    if response.status_code == 401:
        print("There was an error:")
        print("-------------------------------")
        print("ErrorCode:\t" , data.get("errorCode"))
        print("Message:\t" , data.get("message"))
        print("-------------------------------")

    elif response.status_code == 201: 
        print("Login Success")
        token = data.get('created').get('token')
        return token
    else:
        print("There was an internal error:\n")
        print(data)
        return None

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

    if response_2g.status_code == 204 and response_5g.status_code == 204:
        print("Turned on Wifi!")
    else:
        print("There was an error:")
        print(response_2g.json(), "\n", response_5g.json())

def turn_off_wifi(header):
    json = {
        "config":{
            "enable":False,
            "radio":{} 
            } 
        }
    response_2g = session.patch(BAND2G_CONFIG_URL, json=json, headers=header)
    response_5g = session.patch(BAND5G_CONFIG_URL, json=json, headers=header)

    if response_2g.status_code == 204 and response_5g.status_code == 204:
        print("Turned off Wifi!")
    else: 
        print("There was an error :(")
        print(response_2g.json(), "\n", response_5g.json())

def toggle_wifi(header):
    response_2g = session.get(BAND2G_STATE_URL, headers=header)
    response_5g= session.get(BAND5G_STATE_URL, headers=header)
    band2g_state = response_2g.json().get("state").get("enable")
    band5g_state = response_5g.json().get("state").get("enable")

    if band2g_state == True and band5g_state == True:
        turn_off_wifi(header)
    elif band2g_state == False and band5g_state == False:
        turn_on_wifi(header)
    elif band2g_state != band5g_state:
        choice = 0 
        while choice != "1" and choice != "2":
            print("Toggling ambiguous")
            choice = input("Choose whether to turn WIFI on or off:\n 1 - OFF\n 2 - ON\n")
            if choice == "1":
                turn_off_wifi(header)
            elif choice == "2": 
              turn_on_wifi(header)




def logout(token, header):
    DELETE_URL =  BASE_URL + f'/rest/v1/user/3/token/{token}'
    response = session.delete(DELETE_URL, headers=header)

password = input("Enter Password: \n")
token = login(password)
print(token)
if token != None:
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f'Bearer {token}',
        "Content-Type": "application/json"
    }
    toggle_wifi(header)
    logout(token, header) 

