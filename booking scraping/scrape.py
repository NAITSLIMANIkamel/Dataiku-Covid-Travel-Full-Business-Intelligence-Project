from selectorlib import Extractor
import requests 
from time import sleep
from datetime import *
import csv
import sys 
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('booking.yml')

def scrape(url):    
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    try: 
        r = requests.get(url, headers=headers)
        
        if(r.status_code!=200 or len(r.text)<700000):
            return None
        # Pass the HTML of the page and create 

        return e.extract(r.text,base_url=url)
    except:
        return None

# product_data = []
with open(sys.argv[1],'r') as urllist, open('data/'+sys.argv[1].split('/')[-1].split('.')[0]+'.csv','a') as outfile:
    fieldnames = [
        "name",
        "location",
        "city",
        "price",
        "price_for",
        "room_type",
        "beds",
        "rating",
        "rating_title",
        "number_of_ratings",
        "date"
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
    writer.writeheader()
    debut_date=date(2021, 6, 1)
    i=0
    for url in urllist.readlines():
        i+=1
        for deltad in range(0,40):
              daycheckin=debut_date+timedelta(days=deltad*3)
              daycheckout=debut_date+timedelta(days=(deltad*3+1))
              data = scrape(url.format(daycheckin.month,daycheckin.day,daycheckout.month,daycheckout.day))

              if data and data.get('hotels'):
                  for h in data.get('hotels'):
                      h['location']=' '.join(h['location'].split(' ')[:-3])
                      h['date']=daycheckin.isoformat()
                      h ['city']=url.split('&')[0].split('=')[1]
                      writer.writerow(h)
              else :
                break
    print(sys.argv[1],"  ",i)
