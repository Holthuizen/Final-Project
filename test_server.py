import requests
base_url = "http://localhost:9999"

def test_res(base_url, route):
    _url = base_url + route
    resp = requests.get(_url)
    if resp.status_code == 200: 
        print("--> ",_url," | ",resp.text)
    else:
        print("!->ERROR",resp.code,"  ", _url,"  ",resp.text)
        exit()

print("starting")
#create game table
test_res(base_url,"/setup/desperadoes")
#setup players
test_res(base_url,"/join/desperadoes/rutte")
test_res(base_url,"/join/desperadoes/merkel")
test_res(base_url,"/join/desperadoes/putin")
#start game
test_res(base_url,"/begin/desperadoes")
#playing
#round1
test_res(base_url,"/switch/desperadoes/rutte/1/1")
test_res(base_url,"/pass/desperadoes/merkel")
test_res(base_url,"/switch/desperadoes/putin/2/2")
#round2
test_res(base_url,"/switch/desperadoes/rutte/2/2")
#should stop at merkels turn
test_res(base_url,"/switch/desperadoes/merkel/1/1")
test_res(base_url,"/switch/desperadoes/putin/1/1")

