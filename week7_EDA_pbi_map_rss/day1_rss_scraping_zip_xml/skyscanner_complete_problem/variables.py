import json

with open('./credentials.json') as f:
    credentials_gmail = json.load(f)

from_city = "MADR-sky"
to_city = "TYOA-sky"
salida = "2021-07"
llegada = "2021-08"

URL = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-key': "ed20a5eec4msh0f52d1c7ecac524p142a60jsnd882a51f9f9d",
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
}
