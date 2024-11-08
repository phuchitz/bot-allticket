import requests
import time

class ApiFindById():
    def __init__(self, token, name):
        self.token = token
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token,  # replace with actual token
            'priority': 'u=1, i',
            'referer': f'https://www.allticket.com/event/{name}',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

    def get_event_id(self, name):

        # Get the current timestamp in milliseconds
        current_time_ms = int(time.time() * 1000)
        params = {
            'time': current_time_ms,
        }

        # Send the GET request
        url = f'https://www.allticket.com/master/event_info/{name}.json'
        response = requests.get(url, params=params, headers=self.headers)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            event_id = data.get("data", {}).get("event_id")

            # Print the event_id
            if event_id:
                return event_id
            else:
                print("Event ID not found in the response.")
                return None
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None