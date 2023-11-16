import requests
from requests.auth import HTTPBasicAuth

def register(username, password, email, org):
    url = 'https://api.watttime.org/register'
    params = {'username': username,
              'password': password,
              'email': email,
              'org': org}
    rsp = requests.post(url, json=params)
    print(rsp.text)

def login(username, password):
    url = 'https://api.watttime.org/login'
    try:
        rsp = requests.get(url, auth=HTTPBasicAuth(username, password))
    except BaseException as e:
        print('There was an error making your login request: {}'.format(e))
        return None

    try:
        token = rsp.json()['token']
    except BaseException:
        print('There was an error logging in. The message returned from the '
              'api is {}'.format(rsp.text))
        return None

    return token

def get_region_from_loc(token, latitude, longitude, signal_type='co2_moer'):
    url = 'https://api.watttime.org/v3/region-from-loc'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'latitude': latitude, 'longitude': longitude, 'signal_type': signal_type}

    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return rsp.json()

def forecast(token, region, signal_type='co2_moer'):
    url = 'https://api.watttime.org/v3/forecast'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'region': region, 'signal_type': signal_type}
    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return rsp.json()

def forecast_historical(token, region, start, end, signal_type='co2_moer'):
    url = 'https://api.watttime.org/v3/forecast/historical'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {"region": region, "start": start, "end": end, "signal_type": signal_type}
    rsp = requests.get(url, headers=headers, params=params)
    #print(rsp.text)  # uncomment to see raw response
    return rsp.json()

def historical_data(token, region, start, end, signal_type='co2_moer', model=None, updated_since=None):
    url = 'https://api.watttime.org/v3/historical'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'region': region, 'start': start, 'end': end, 'signal_type': signal_type, 'model': model, 'updated_since':updated_since}

    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return rsp.json()

# account details
username = 'YOUR USERNAME HERE'
password = 'YOUR PASSWORD HERE'
email = 'some_email@gmail.com'
org = 'some org name'

# request details
latitude = 37.8720
longitude = -122.2578
region = 'CAISO_NORTH'  # identify grid region
start = '2023-07-01T00:00:00-0000'  # UTC offset of 0
end = '2023-07-01T04:00:00-0000'

# Only register once!!
# register(USERNAME, PASSWORD, EMAIL, ORG)

token = login(username, password)
if not token:
    print('You will need to fix your login credentials (username and password '
          'at the start of this file) before you can query other endpoints. '
          'Make sure that you have registered at least once by uncommenting '
          'the register(username, password, email, org) line')
    exit()
    
location = get_region_from_loc(token, latitude, longitude)
print(location)
    
forecast_moer = forecast(token, region)
print(forecast_moer)

forecast_moer_historical = forecast_historical(token, region, start, end)
print(forecast_moer_historical)

historical_moer = historical_data(token, region, start, end)
print(historical_moer)
