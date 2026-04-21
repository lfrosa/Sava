import os
import urllib.request
import json
import winreg

k = os.environ.get('GEMINI_API_KEY')
if not k:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as reg:
            k, _ = winreg.QueryValueEx(reg, 'GEMINI_API_KEY')
    except:
        pass
if k:
    try:
        req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models?key=' + k)
        req.add_header('Accept', 'application/json')
        res = json.loads(urllib.request.urlopen(req).read())
        print([m['name'] for m in res['models']])
    except Exception as e:
        print("API Error:", e)
else:
    print('No key')