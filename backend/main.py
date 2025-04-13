from fastapi import FastAPI, Response, Header
import wifi
import uvicorn 

app = FastAPI()
PASSWORD_FILE = "secrets/password"
API_KEY_FILE = "secrets/apikey"
PASSWORD = ""
API_KEY = ""
with open(PASSWORD_FILE, "r") as f:
    PASSWORD = f.read().strip()
with open(API_KEY_FILE, "r") as f:
    API_KEY = f.read().strip()
if API_KEY == "":
    raise Exception("No apikey set")
if PASSWORD == "":
    raise Exception("No password set")

@app.get("/status")
def get_status(apikey: str = Header(None)):
    if apikey != API_KEY:
        return Response(status_code=401)

    token = wifi.login(PASSWORD)
    header = wifi.get_header(token)
    state_5g = wifi.get_state(header, '5g')
    state_2g = wifi.get_state(header, '2g')
    wifi.logout(token)
    if state_2g or state_5g:
        return Response(status_code=200)
    else:
        return Response(status_code=204)

@app.post("/toggle")
def toggle_wifi(apikey: str = Header(None)):
    if apikey != API_KEY:
        return Response(status_code=401)

    token = wifi.login(PASSWORD)
    header = wifi.get_header(token)
    response_2g, response_5g  = wifi.toggle_wifi(header)
    logout_response = wifi.logout(token)
    if response_2g.ok and response_5g.ok:
        return Response(status_code=200)
    else:
        return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
