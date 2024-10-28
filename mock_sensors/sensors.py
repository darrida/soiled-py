import random

import requests

sensors = [
    "12:23:34:45:56:67",
    "12:34:56:78:90:12",
    "09:89:98:98:75:21",
    "76:65:54:43:32:21",
    "21:09:87:65:43:32",
    "76:65:54:43:32:25"
]

for _ in range(30):
    for sensor in sensors:
        response = requests.post(
            "http://localhost:8000/api/soiled/measurement/",
            headers={'Authorization': 'Bearer supersecret'},
            json={
                "mac_address": sensor,
                "moisture_percent": random.randint(70, 100),  # noqa: S311
            },
            timeout=5
        )
        if response.status_code == 204:
            response = requests.post(
                "http://localhost:8000/api/soiled/sensor/",
                headers={'Authorization': 'Bearer supersecret'},
                json={"mac_address": sensor},
                timeout=5
            )
            print(response.status_code)
            print(response.text)
            print(f"{sensor} created in system. Login to admin and associate a plant with the sensor.")
        elif response.status_code == 206:
            print(response.text)
