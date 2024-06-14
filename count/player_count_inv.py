import time
import requests


#https://api.battlemetrics.com/servers/27255969 - "[RU] [RFS: INV] Russian Freedom Server"
def get_player_count(server_id):
    url = f"https://api.battlemetrics.com/servers/{server_id}"
    response = requests.get(url)
    data = response.json()
    return data['data']['attributes']['players']


def main():
    server_id = "27255969"  # Идентификатор сервера
    interval = 600  # Интервал времени в секундах (10 минут)

    while True:
        try:
            players_count = get_player_count(server_id)
            print(f"Current player count: {players_count}")
        except Exception as e:
            print(f"Error fetching player count: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    main()
