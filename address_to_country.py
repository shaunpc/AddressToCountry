def geocoding_lookup(gl_api_key, address):
    """
    Returns the response JSON payload of a location using the Google Maps Geocoding API.
    API: https://developers.google.com/maps/documentation/geocoding/start
    """
    import requests
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ', '+'), gl_api_key))
    resp_json_payload = {}
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
    except:
        print(Fore.RED + 'ERROR: {}'.format(address))
    return resp_json_payload


def country_resolver(json):
    """
    Returns the short name variant of the Country from the JSON address payload
    """

    final = {}
    if json['results']:
        data = json['results'][0]
        for item in data['address_components']:
            for category in item['types']:
                data[category] = {}
                data[category] = item['short_name']
        final['street'] = data.get("route", None)
        final['state'] = data.get("administrative_area_level_1", None)
        final['city'] = data.get("locality", None)
        final['county'] = data.get("administrative_area_level_2", None)
        final['country'] = data.get("country", None)
        final['postal_code'] = data.get("postal_code", None)
        final['neighborhood'] = data.get("neighborhood", None)
        final['sublocality'] = data.get("sublocality", None)
        final['housenumber'] = data.get("housenumber", None)
        final['postal_town'] = data.get("postal_town", None)
        final['subpremise'] = data.get("subpremise", None)
        final['latitude'] = data.get("geometry", {}).get("location", {}).get("lat", None)
        final['longitude'] = data.get("geometry", {}).get("location", {}).get("lng", None)
        final['location_type'] = data.get("geometry", {}).get("location_type", None)
        final['postal_code_suffix'] = data.get("postal_code_suffix", None)
        final['street_number'] = data.get('street_number', None)

    return final['country']


def process_csv_file(filename, pcf_api_key):
    """
    Reads each line in the passed file, and performs country geocode lookup
    """
    import csv
    count_match = 0
    count_mismatch = 0
    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            address = row[0]
            expected = row[1].replace('"', '').strip()
            # print('ADDRESS=%s' % address)

            # get google maps geocoder details
            json_payload = geocoding_lookup(pcf_api_key, address)
            # print('PAYLOAD=%s' % json_payload)

            # decode it to get just country code
            country = country_resolver(json_payload)

            if country == expected:
                str1 = Fore.GREEN + 'MATCH:' + Fore.RESET + ' COUNTRY=' + Fore.GREEN + country
                str2 = Fore.RESET + ' [EXPECTED=' + Fore.CYAN + expected + Fore.RESET + '] ADDRESS:' + address
                print(str1 + str2)
                count_match = count_match + 1
            else:
                str1 = Fore.RED + 'DIFF:' + Fore.RESET + ' COUNTRY=' + Fore.RED + country
                str2 = Fore.RESET + ' [EXPECTED=' + Fore.CYAN + expected + Fore.RESET + '] ADDRESS:' + address
                print(str1 + str2)
                count_mismatch = count_mismatch + 1
    print('PROCESSED %d RECORDS: %d MATCH, %d MISMATCH' % (count_match + count_mismatch, count_match, count_mismatch))
    return


if __name__ == '__main__':
    # init colorama
    from colorama import init

    init(autoreset=True)
    from colorama import Fore

    # get key - DO NOT STORE THIS FILE IN GITHUB REPO!
    file_api_key = 'api_key.txt'
    file = open(file_api_key, 'r')
    api_key = file.read()
    # print('API_KEY=%s' % api_key)

    # CSV Format
    #  "address-to-test", expected-country-code

    file_addresses = 'address_list.csv'
    print('SOURCE=%s' % file_addresses)

    process_csv_file(file_addresses, api_key)
