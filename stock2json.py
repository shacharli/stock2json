import requests
from bs4 import BeautifulSoup
import json
import sys


def main():
    symbol = sys.argv[1]
    url = 'https://www.marketwatch.com/investing/stock/' + symbol
    try: 
        r = requests.get(url)
          
        data= {}
        soup = BeautifulSoup(r.text, 'html.parser')
        
        price_coin = soup.find('h2', attrs={'class': 'intraday__price'}).text.strip("\n")
        
        try :
            if price_coin[0]!="-":
                int(price_coin[0])
            data["price"] = price_coin
            data["currency"] = ""
            
        except:
            data["price"] = price_coin[1:].strip("\n")
            data["currency"] = price_coin[0]
            
        data["last updated"] = soup.find('span', attrs={'class': 'timestamp__time'}).text[14:]
        data['status']= soup.find('div', attrs={'class': 'status'}).text
        data["point_change"]= soup.find('span', attrs={'class': 'change--point--q'}).text
        data["percent_change"] = soup.find('span', attrs={'class': 'change--percent--q'}).text
        data["returnAnswer"] = "true"      
        print ("you requested the data for", symbol, ", got it!")
        
    except:
        data["returnAnswer"] = "false"
        print ("you requested the data for", symbol, ", but it is not available")
        
    with open(symbol+'.json', 'w') as f:
        json.dump(data, f)
    
if __name__ == '__main__':
    main()