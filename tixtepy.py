import requests

url = "https://api.tixte.com/v1/"

# why are you reading this??

class tixtepy():

    global hasInitialised
    hasInitialised = False;

    hasInitialised = False
    global apiKey
    global authKey

    # initialise connection because i dont want to pass api key and auth to every fucking method
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


    # it gets domains 
    def GetDomains():
        # early return if not init
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return

        # try catch my beloved

        try:
            r = requests.get(url + "users/@me/domains", headers=data)

            # make the object json
            resJSON = r.json()
            
            # get the data key (i dont care about status :) )
            res = resJSON["data"]

            # Essentially return res['data']['domains'] but idk how to do that in one line kms
            return res["domains"]
        
        # website down lol
        except Exception as e:
            return e

    # gets domains
    # Method takes a string - le "domain" - and uhh finds info on it 
    def GetDomainInfo(domain):
        
        # early return w/e
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return

        try:
            r = requests.get(url + "users/@me/domains", headers=data)

            # Same method to get to the juicy stuff as before, also im stupid :+1:
            rJSON = r.json()

            response = rJSON['data']
            domains = response['domains']

            # Easiest way I could think of to scan through all domains on your account to find the one you want
            for object in domains:
                if not object['name'] == domain:
                    continue
                else:
                    return object
        except Exception as e :
            return e

    # you get the idea
    def GetAccountInfo():
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        try:
            r = requests.get(url + "users/@me/uploads/size", headers=data)

            resJSON = r.json()
            resData = resJSON['data']

            premium_tier = resData['premium_tier']

            # Server response (resData) gives back uploadlimit in bytes. 
            # too lazy to figure out how many bytes in a gb? same. 
            if premium_tier == 0:
                UploadLimit = 15
            elif premium_tier == 1:
                UploadLimit = 200
            elif premium_tier == 2:
                UploadLimit = 500

            usedBytes = resData['used']
            # I know I said I'm too lazy before, but this a dynamic value so I had to do a little "math"
            usedGb = round(float(usedBytes / 1000000000), 2)

            # Return essentially the same object I got from the server lol
            return [{'premium_tier': premium_tier, 'UploadLimit': UploadLimit, 'UsedSpace': usedGb}]
        except Exception as e:
            return e 

    # !! DANGEROUS METHOD
    # There is no confirmation built into this framework prevent accidentally deleting a domain.
    # 
    # Method takes string of le "domain" and promptly deletes it 
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
        except Exception as e:
            return e

    # The first actually useful method lawl
    # Essentially just gets the last few uploads you put on tixte
    #
    # method takes int amount to fetch
    # i.e amount=3 will return last 3 screenshots
    #
    # default amount is 48 because thats what it is on tixte
    def GetRecentUploads(amount=48):
        if not hasInitialised:
            print("No api key or authorization provided!\nPlease run tixtepy.init(\"apiKey\" \"authKey\") first!")
            return
        
        try:
            r = requests.get(url + f'users/@me/uploads?page=0&amount={amount}&permission_levels=[3]', headers = data)

            rJSON = r.json()
            resData = rJSON['data']
            resUploads = resData['uploads']
            
            for object in resUploads :  
                del object['type']
                del object['asset_id']
                del object['permission_level']
                del object['expiration']
            
            return resUploads
        
        except Exception as e :
            return e