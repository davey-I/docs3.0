from string import Template
import os
from bs4 import BeautifulSoup as bs
from find_string_start import find_string

path = "./pages"
rep = '''<svg class="add-tag-icon" xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <!-- < and > symbols -->
  <path d="M6 8l-4 4 4 4" /> <!-- Left angle bracket -->
  <path d="M18 8l4 4-4 4" /> <!-- Right angle bracket -->

  <!-- Plus sign in center -->
  <path d="M12 10v4" />
  <path d="M10 12h4" />
</svg>
'''

for root, dirs, files in os.walk("./pages"):


    if len(dirs) == 0:


        for i in files:

            pfad = root+"/"+i

            with open(pfad, "r", encoding="utf-8") as f:
                soup = bs(f, "html.parser")
                for btn in soup.find_all("button", class_="create-subdiv"):
                    btn.clear()
                    btn.append(bs(rep, "html.parser"))

            with open(pfad, 'w', encoding='utf-8') as f:
                
                f.write(str(soup))
                    