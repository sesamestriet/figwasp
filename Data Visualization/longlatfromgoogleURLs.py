from IPython.display import display
import pandas as pd

url = pd.read_excel('Google Maps_ Hindu Temples in Hawaii.xlsx')

   
def urlsplit(x):
    x = x.split("!3d")[1].split("!16s")[0].split("!4d")
    return (x)

url['coordinates'] = [urlsplit(x) for x in url['FTb5Zb src']]

url[['latitude', 'longitude']] = url['coordinates'].apply(pd.Series)

#print(url[['latitude', 'longitude']])

#url.to_excel('Google Maps_ Hindu Temples in Hawaii.xlsx')

url_test = 'https://www.google.com/maps/place/White+Sands+Buddhist+Center/data=!4m7!3m6!1s0x88e74a11c4a37a57:0xe3feb348f1b3a76b!8m2!3d28.725554!4d-80.8838169!16s%2Fg%2F1thl1pfz!19sChIJV3qjxBFK54gRa6ez8Uiz_uM?authuser=0&hl=en&rclk=1'
lat_lon = url_test.split("!3d")[1].split("!16s")[0].split("!4d")
print(lat_lon)