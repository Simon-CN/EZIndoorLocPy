import urllib.request
from bs4 import BeautifulSoup

url = 'http://106.37.208.228:8082/'
res = urllib.request.urlopen(url).read()
s = res.decode()

soup = BeautifulSoup(s)
print(soup.prettify())

ctr = soup.find(id='contaniner')
scp = ctr.contents
