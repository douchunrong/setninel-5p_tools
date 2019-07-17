import datetime
import json
from requests import Session
from requests.auth import HTTPBasicAuth


#Products constants
OZONE_TOTAL = 'L2__O3____'
OZONE_TROPOSPHIRIC = 'L2__O3_TCL'
OZONE_PROFILE = 'L2__O3__PR'
OZONE_TROPOSPHIRIC_PROFILE = 'L2__O3_TPR'
NITROGEN_DIOXIDE = 'L2__NO2___'
SULFAR_DIOXIDE = 'L2__SO2___'
CARBON_MONOXID = 'L2__CO____'
METHANE = 'L2__CH4___'
FORMALDEHYDE = 'L2__HCHO__'


def s5_quarry(days = '', wkt = '', product_type = '', ingestion_date_FROM = '', ingestion_date_TO = '', full_response = False ):
    login = 's5pguest'
    password = 's5pguest'

    quarry = ''
    #Setting up payload for auth
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {"login_username": 's5pguest',
               "login_password": 's5pguest'}

    #Auth
    with Session() as s:
        s.post('https://s5phub.copernicus.eu/dhus////login', data = payload, auth=HTTPBasicAuth(login, password), headers = headers)
        # Performing quarry depending on parameters

        #Quarring data for last X days
        if days != '':
            days = int(days) * -1
            ingestion_date_TO = datetime.datetime.now()
            ingestion_date_FROM = ingestion_date_TO + datetime.timedelta(days)
            ingestion_date_TO = str(ingestion_date_TO.date())
            ingestion_date_FROM = str(ingestion_date_FROM.date())

            #Quaring data intersecting the WKT object
            if wkt != '':
                #Quarring specific product type data
                if product_type != '':
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
                             '(%20footprint:%22Intersects(' + wkt + \
                             ')%22)%20AND%20' + '(%20ingestionDate:[' + ingestion_date_FROM + \
                             'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)' + \
                             '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:' + product_type + \
                             '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
                #Quarring all data products
                else:
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter='\
                             + '(%20footprint:%22Intersects(' + wkt + \
                             ')%22)%20AND%20' + '(%20ingestionDate:[' + ingestion_date_FROM + \
                             'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'
            #Quarring data
            else:
                #Quarring specific product type data
                if product_type != '':
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
                             + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)' + '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:'\
                             + product_type + '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
                # Quarring all data products
                else:
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
                             + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'

        else:

            if wkt != '':
                if product_type != '':
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
                             '(%20footprint:%22Intersects(' + wkt + ')%22)%20AND%20' + '(%20ingestionDate:['\
                             + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)' + '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:'\
                             + product_type + '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
                else:
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
                             '(%20footprint:%22Intersects(' + wkt + ')%22)%20AND%20' + \
                             '(%20ingestionDate:[' + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'
            else:
                if product_type != '':
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
                             + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20'\
                             + ingestion_date_TO + 'T23:59:59.999Z%20]%20)' + \
                             '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:' + product_type + \
                             '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
                else:
                    quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
                             + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
                             'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'

        r = s.get(quarry, headers=headers)
        resp = json.loads(r.text)

        if full_response == False:
            products = []
            for p in resp['products']:
                product = {
                    'identifier': p['identifier'],
                    'uuid': p['uuid'],
                    'date': p['summary'][0][7:-14]
                }
                products.append(product)
            return products

        else:
            return resp



def download_product(uuid, output_path):

    url = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('" + str(uuid) + "')/$value"

    login = 's5pguest'
    password = 's5pguest'

    # Setting up payload for auth
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {"login_username": 's5pguest',
               "login_password": 's5pguest'}

    # Downloading file auth request
    with Session() as s:
        s.post('https://s5phub.copernicus.eu/dhus////login', data=payload, auth=HTTPBasicAuth(login, password),
               headers=headers)
        r = s.get(url, headers=headers)
        filname = r.headers['Content-Disposition'][17:-1]

        with open(output_path + filname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    print('Downloading...')





