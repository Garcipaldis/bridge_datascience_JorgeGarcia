
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import pandas as pd
import requests


def call_api(from_city, to_city, salida, llegada, URL, headers):
    url_service = URL + "apiservices/browsedates/v1.0/ES/USD/ma-ES/" + from_city + "/" + to_city + "/" + salida + "/" + llegada

    response = requests.request("GET", url_service, headers=headers)

    return response.json()


def get_quotes(resp_jon):
    quotes_json = resp_jon['Quotes']

    tot_quotes = {'QuoteId': [],
                  'OriginId': [],
                  'DestinationId': []
                  }

    for quote in quotes_json:
        quote_id = quote.get('QuoteId', None)
        origin_id = quote.get('OutboundLeg', None).get('OriginId', None)
        destination_id = quote.get('OutboundLeg').get('DestinationId', None)

        tot_quotes['QuoteId'].append(quote_id)
        tot_quotes['OriginId'].append(origin_id)
        tot_quotes['DestinationId'].append(destination_id)

    return pd.DataFrame(tot_quotes)



def get_places(resp_jon):
    places_json = resp_jon['Places']

    tot_places = {'PlaceId': [],
                  'SkyscannerCode': [],
                  'CityName': []
                  }

    for quote in places_json:
        place_id = quote.get('PlaceId', None)
        skyscannercode = quote.get('SkyscannerCode', None)
        city_name = quote.get('CityName', None)

        tot_places['PlaceId'].append(place_id)
        tot_places['SkyscannerCode'].append(skyscannercode)
        tot_places['CityName'].append(city_name)

    return pd.DataFrame(tot_places)


def get_dates_one_way(dates_json, out_in):
    tot_dates = {'Date_' + out_in: [],
                 'Price_' + out_in: [],
                 'QuoteDateTime_' + out_in: [],
                 'QuoteId': []
                 }

    for quote in dates_json:
        partial_date = quote.get('PartialDate', None)
        price = quote.get('Price', None)
        quote_date = quote.get('QuoteDateTime', None)
        quite_ids = quote.get('QuoteIds', None)

        for j in quite_ids:
            tot_dates['Date_' + out_in].append(partial_date)
            tot_dates['Price_' + out_in].append(price)
            tot_dates['QuoteDateTime_' + out_in].append(quote_date)
            tot_dates['QuoteId'].append(j)

    return pd.DataFrame(tot_dates)


def get_dates(resp_jon):
    dates_json = resp_jon['Dates']

    dates_outbound = get_dates_one_way(dates_json['OutboundDates'], 'Out')
    dates_inbound = get_dates_one_way(dates_json['InboundDates'], 'In')

    return dates_outbound, dates_inbound




def send_mail(from_mail, password, to_mail, subject, body):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_mail
    message['To'] = to_mail

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], password)
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()
