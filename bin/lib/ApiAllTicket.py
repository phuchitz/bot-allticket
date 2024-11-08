import requests
import time


class ApiAllTicket:
    def __init__(self, token, event_name):
        self.token = token
        self.base_url = 'https://www.allticket.com/api-booking/'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'atk-z-data': 'U2FsdGVkX1+y6uLMshmnK/Upgm1U4+vhS+azhfNh31uXZvEZrl5SrrmI2DoJPAh+BTgFK422j1Fwlogm56pcQ1tRSVUtHMykqpRRslRNZMxcLu+r9mtV9lthbLnIUSpo39jxuXgMjwFx0uLIEexui9OTpNB6oTxXHpaBhTw7KS2hs3c7O1YVo9ljSdWzK8To',
            'authorization': self.token,
            'content-type': 'application/json',
            'origin': 'https://www.allticket.com',
            'priority': 'u=1, i',
            'referer': f'https://www.allticket.com/event/{event_name}',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }

    def get_seats(self, perform_id, round_id, zone_id, number_of_seats):
        """ดึงที่นั่งที่ว่างจาก API"""
        url = f'{self.base_url}get-seat'
        payload = {'performId': perform_id, 'roundId': round_id, 'zoneId': zone_id}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            seat_data = response.json().get("data", {}).get("seats_available", [])

            available_seats = [
                f"{seat['rowName']}_{seat['seatNo']}"
                for zone in seat_data
                for seat in zone['seat']
                if seat['status'] == "A"
            ]
            return available_seats[:number_of_seats]

        except requests.RequestException as e:
            print(f"Error getting seats: {e}")
            return []

    def handler_reserve(self, perform_id, zone_id, round_id, seats):
        """ดำเนินการจองที่นั่ง"""
        url = f'{self.base_url}handler-reserve'
        payload = {
            'performId': perform_id,
            'roundId': round_id,
            'zoneId': zone_id,
            'screenLabel': zone_id,
            'seatTo': {
                'seatType': 'SEAT',
                'seats': seats
            },
            'shirtTo': [],
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get("data", {}).get("uuid")

        except requests.RequestException as e:
            print(f"Error reserving seats: {e}")
            return None
