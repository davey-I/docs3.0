from string import Template
import os
from bs4 import BeautifulSoup as bs

path = "./pages/Linux/Must-Have-Tools.html"
stringy = "disk"
with open(path, 'r', encoding='utf-8') as f:
  soup = bs(f, 'html.parser')

soup = soup.find_all('p')

for td in soup:
    ptext = td.get_text()
    
    lines = ptext.splitlines()

    for line in lines:
      if(stringy in line):
        print(line.strip())