

from utils import call_api, get_quotes, get_places, send_mail, get_dates
from pretty_html_table import build_table
from variables import *


def main():
    # CALL API
    resp_jon = call_api(from_city, to_city, salida, llegada, URL, headers)

    # QUOTES
    quotes_df = get_quotes(resp_jon)

    # PLACES
    places_df = get_places(resp_jon)

    # DATES
    inbound_df, outbound_df = get_dates(resp_jon)


    ########################################
    #### MERGE  ############################
    ########################################
    all_data = quotes_df.merge(inbound_df, how='left', on='QuoteId')
    all_data = all_data.merge(outbound_df, how='left', on='QuoteId')
    all_data['Price tot'] = all_data['Price_Out'] + all_data['Price_In']

    all_data = all_data.merge(places_df[['PlaceId', 'CityName']], left_on='OriginId', right_on='PlaceId')
    all_data.drop(columns = ['PlaceId'], inplace=True)

    all_data = all_data.merge(places_df[['PlaceId', 'CityName']], left_on='DestinationId', right_on='PlaceId')
    all_data.drop(columns = ['PlaceId'], inplace=True)
    all_data.rename(columns={'CityName_x': 'Origin',
                            'CityName_y': 'Destination'},
                    inplace=True)

    all_data.sort_values(by=['Price tot'], inplace=True)
    all_data.drop(columns = ['QuoteId', 'OriginId', 'DestinationId'], inplace=True)


    ########################################
    ###### MAIL ############################
    ########################################

    subject = 'Novedades vuelos'

    send_mail(credentials_gmail['mail'],
            credentials_gmail['password'],
            credentials_gmail['mail'],
            subject,
            build_table(all_data, 'blue_light'))


if __name__ == "__main__":
    main()
