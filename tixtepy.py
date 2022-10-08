from shutil import ExecError
import requests

url = "https://api.tixte.com/v1/"

class tixtepy():

    global hasInitialised
    hasInitialised = False;

    hasInitialised = False
    global apiKey
    global authKey

    def init(api_key, auth):
        global hasInitialised
        hasInitialised = True
        global apiKey
        apiKey = api_key

        global authKey
        authKey = auth

        global data
        data = {

            'authorization':authKey,
            'x-api-sitekey':apiKey
        }


    def GetDomains():
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        
        print("Fetching..")

        try:
            r = requests.get(url + "users/@me/domains", headers=data)

            print(r.text)

            resJSON = r.json()
            res = resJSON["data"]

            return res["domains"]
        
        except Exception:
            return Exception

    def GetDomainInfo(domain):
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        try:
            r = requests.get(url + "users/@me/domains", headers=data)

            rJSON = r.json()

            response = rJSON['data']
            domains = response['domains']

            for object in domains:
                if not object['name'] == domain:
                    continue
                else:
                    return object
        except Exception:
            return Exception

    def GetAccountInfo():
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        try:
            r = requests.get(url + "users/@me/uploads/size", headers=data)

            resJSON = r.json()
            resData = resJSON['data']

            premium_tier = resData['premium_tier']

            if premium_tier == 0:
                UploadLimit = 15
            elif premium_tier == 1:
                UploadLimit = 200
            elif premium_tier == 2:
                UploadLimit = 500

            usedBytes = resData['used']
            usedGb = round(float(usedBytes / 1000000000), 2)

            return [{'AccountLevel': premium_tier, 'UploadLimit': UploadLimit, 'UsedSpace': usedGb}]
        except Exception:
            return Exception

    def DeleteDomain(domain):
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        
        try:
            r = requests.delete(url + "users/@me/domains/" + domain, headers = data)

            rJSON = r.json()
            status = rJSON['success']

            if not status == True:
                print("Could not delete domain, likely doesn't exist")
                return

            return rJSON['data']
        except Exception:
            return Exception