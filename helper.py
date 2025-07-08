from string import Template
import os
from bs4 import BeautifulSoup as bs
from find_string_start import find_string

path = "./pages"
rep = '''<svg xmlns="http://www.w3.org/2000/svg" class="wrench-icon" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
  <path d="M22.7 19.3l-4.1-4.1c.6-1.1.9-2.3.9-3.5 0-3.9-3.1-7-7-7-1.3 0-2.5.3-3.5.9l3.3 3.3-4 4-3.3-3.3C4.3 10.5 4 11.7 4 13c0 3.9 3.1 7 7 7 1.3 0 2.5-.3 3.5-.9l4.1 4.1c.4.4 1 .4 1.4 0l2.7-2.7c.4-.4.4-1 0-1.4z"/>
</svg>
'''

for root, dirs, files in os.walk("./pages"):


    if len(dirs) == 0:


        for i in files:

            pfad = root+"/"+i

            with open(pfad, "r", encoding="utf-8") as f:
                soup = bs(f, "html.parser")
                for btn in soup.find_all("button", class_="foldable-content-edittoggle"):
                    btn.clear()
                    btn.append(bs(rep, "html.parser"))


            with open(pfad, 'w', encoding='utf-8') as f:
                f.write(str(soup))
