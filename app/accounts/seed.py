import json
import requests
from .address import Address, Lga, State
from django.db import transaction


drive_file_url = (
    "https://drive.google.com/file/d/1Ev-iYNXDtehXzC5w4qYXXeAZ_62ALBQU/view?usp=sharing"
)
drive_file_id = "1Ev-iYNXDtehXzC5w4qYXXeAZ_62ALBQU"
download_url = f"https://drive.google.com/uc?id={drive_file_id}"


@transaction.atomic
def seed_database(json_url=download_url):

    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to fetch JSON data. Status code: {response.status_code}")

    for state_name, districts in data.items():
        state = State.objects.create(name=state_name.title())
        for district_details, lgas in districts.items():
            for lga in lgas:
                Lga.objects.create(name=lga.title(), state=state)

    print("Database seeded successfully")


seed_database()
