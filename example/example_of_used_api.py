import requests


URL_AUTH = "https://developers.lingvolive.com/api/v1.1/authenticate"  # const

URL_TRANSLATE = "https://developers.lingvolive.com/api/v1/Minicard"

#  KEY = "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk56TTVOREV6TVRRc0lrMXZaR1ZzSWpwN0lrTm9ZWEpoWTNSbGNuTlFaWEpFWVhraU9qVXdNREF3TENKVmMyVnlTV1FpT2pjME1EVXNJbFZ1YVhGMVpVbGtJam9pTmpreE4yWTNaV010TkRjelpDMDBPVEExTFRsa01UWXRPVFEyWWpZMk1tRmhNVEl4SW4xOS41d2pTRjczU19rM2ZnT0M5SmxMZVBYQzFWdkk0Tm5QOUZ4WHRqUl9EaFV3"

KEY = "NjkxN2Y3ZWMtNDczZC00OTA1LTlkMTYtOTQ2YjY2MmFhMTIxOjA1ODZkZTNkNDg3NzRiZmU5MWJiNDdkYjY1ZWZlOWY0"

headers_auth = {"Authorization": "Basic " + KEY}

auth = requests.post(URL_AUTH, headers=headers_auth)

if auth.status_code == 200:
    token = auth.text
    print(token)
    while True:
        word = input("Введите слово для перевода: ")
        if word:
            print(word)
            headers_translate = {
                "Authorization": "Bearer " + token,
            }
            params =  {
                "text": word,
                "srcLand": 1033,
                "dstLand": 1049,
            }
            r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
            res = r.json()
            print(res)
            try:
                print(res["Translation"]["Translation"])
            except:
                print("Не найдено")
else:
    print("Error!")


# do not work
