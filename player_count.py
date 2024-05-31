import subprocess
import time
import requests

#Скрипт выключающий компьютер, по достижению 80 человек на сервере
peak = 80

while True:
    response = requests.get("https://api.battlemetrics.com/servers/26737505")
    data = response.json()
    players_count = data['data']['attributes']['players']
    if players_count > peak:
        subprocess.run(['shutdown', '/s'])
    time.sleep(600)
