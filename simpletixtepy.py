import requests

url = "https://api.tixte.com/v1/"

class simpletixtepy():

    # initialise connection because i dont want to pass api key and auth to every fucking method

    def __init__(self, api_key : str, auth : str) -> None:
        self.api_key = api_key
        self.auth = auth

        self.data = {
            'authorization': auth,
            'x-api-sitekey': api_key
        }

    # it gets domains 
    def GetDomains(self):
        # try catch my beloved
        try:
            r = requests.get(url + "users/@me/domains", headers=self.data)

            # make the object json
            resJSON = r.json()
            
            # return le domains
            return resJSON['data']['domains']
        
        # website down lol
        except Exception as e:
            return e

    # gets domains
    # Method takes a string - le "domain" - and uhh finds info on it 
    def GetDomainInfo(self, domain : str):
        try:
            r = requests.get(url + "users/@me/domains", headers=self.data)

            # Same method to get to the juicy stuff as before, also im stupid :+1:
            rJSON = r.json()

            domains = rJSON['data']['domains']

            # Easiest way I could think of to scan through all domains on your account to find the one you want
            for object in domains:
                if not object['name'] == domain:
                    continue
                else:
                    return object
        except Exception as e :
            return e

    # you get the idea
    def GetAccountInfo(self):
        try:
            r = requests.get(url + "users/@me/uploads/size", headers=self.data)

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
            # I know I said I'm too lazy before, but self a dynamic value so I had to do a little "math"
            usedGb = round(float(usedBytes / 1000000000), 2)

            # Return essentially the same object I got from the server lol
            return [{'premium_tier': premium_tier, 'UploadLimit': UploadLimit, 'UsedSpace': usedGb}]
        except Exception as e:
            return e 

    # !! DANGEROUS METHOD
    # There is no confirmation built into self framework prevent accidentally deleting a domain.
    # 
    # Method takes string of le "domain" and promptly deletes it 
    def DeleteDomain(self, domain):
        try:
            r = requests.delete(url + "users/@me/domains/" + domain, headers = self.data)

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
    def GetRecentUploads(self, amount: int = 48):
        try:
            r = requests.get(url + f'users/@me/uploads?page=0&amount={amount}&permission_levels=[3]', headers = self.data)

            rJSON = r.json()
            resUploads = rJSON['data']['uploads']
            
            # Deleting keys I couldn't find a real use for. I only delete these as I don't think they are really used in v1 of the tixte api anyway
            for object in resUploads :  
                del object['type']
                del object['permission_level']
                del object['expiration']
            
            return resUploads
        
        except Exception as e :
            return e

    # Deletes a file, given the file name or id (without the file extension)
    def DeleteFile(self, string: str):
        try:
            r = requests.delete(url + f'users/@me/uploads/{string}', headers = self.data)

            rJSON = r.json()

            if rJSON['success'] == True :
                return rJSON

            recent = self.GetRecentUploads(50)

            for item in recent:
                if not item['name'] == string:
                    continue
                else:
                    id = item['asset_id']
                    r = requests.delete(url + f'users/@me/uploads/{id}', headers = self.data)

                    return r.json()

        except Exception as e: 
            return e

    # uploads file to tixte :)
    # methods take string of file path, and strina of domain to upload to
    # nya
    def UploadFile(self, file : str, domain : str):
        try:
            files = {
                'file': (file, open(file, 'rb')),
            }

            self.data.update({'domain': domain})

            r = requests.post(url + 'upload', headers = self.data, files=files, data=self.data)

            return r.json()
        except Exception as e:
            return e

#Work in progress here
class simpletixteembed():
    
    def __init__(self, api_key : str, auth : str) -> None:
        self.data = {
            'authorization': auth,
            'x-api-sitekey': api_key
        }
    
    def getEmbedDetails(self):
        r =  requests.get(url + "users/@me/config")

        rJSON = r.json()
        return rJSON