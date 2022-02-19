import math
import pycountry
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myApp")

class tweetCountries:
    def __init__(self, country, code, support, unsupport, count):
        self.country = country
        self.code = code
        self.support = support
        self.unsupport = unsupport
        self.count = count
    
    def get_country(self):
        return self.country
    
    def get_support(self):
        return self.support

    def get_unsupport(self):
        return self.unsupport


def getAddress(loc):
    location = geolocator.geocode(loc, language="en")
    lat = location.latitude
    long = location.longitude
    return (lat, long)

def getCountry(loc):
    try:
        (lat, long) = getAddress(loc)
        location = geolocator.reverse([lat, long])
        country = location.raw['address']['country_code']
    except:
        country = "Not Found"
    return country



def getCountryList(tweets, countries):
    print("GETTING THE COUNTRY :")
    countryList = [] 
    for country in countries:
        if country != "Not Found":
            try:
                countryNow = pycountry.countries.get(alpha_2=country)
                support = 0
                unsupport = 0
                counter = 0
                for tweet in tweets:
                    if tweet['Country'] == country:
                        if tweet['opinion'] == 'Support':
                            counter += 1
                            support += 1
                        elif tweet['opinion'] == 'Unsupport':
                            counter += 1
                            unsupport += 1
                print("GETTING THE RESULT :")
                support_rate = str(round_decimals_up((support/(support + unsupport))*100)) + "%"
                unsupport_rate = str(round_decimals_up((unsupport/(support + unsupport))*100)) + "%"
                # get the country name
                coutryName = countryNow.name
                # get the country code by 3 digits
                code = countryNow.alpha_3
                print("GETTING THE RESULT :" + str(support_rate))
                countryList.append(tweetCountries(coutryName, code, support_rate, unsupport_rate, counter))
            except:
                print("IN ERROR: " + country)
    return countryList




def round_decimals_up(number:float, decimals:int=1):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor