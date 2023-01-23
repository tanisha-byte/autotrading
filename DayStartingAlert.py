import requests
from bs4 import BeautifulSoup

data = URL = "https://kite.zerodha.com/dashboard"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
print(soup.prettify()) 