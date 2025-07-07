import os
from bs4 import BeautifulSoup

def find_string(input):
  path = "./pages"
  search_word = input
  context_words = 6  # number of words to show after match
  
  def extract_paragraphs(file_path):
      with open(file_path, "r", encoding="utf-8") as f:
          soup = BeautifulSoup(f, "html.parser")
          return [
              div.get_text(separator=" ", strip=True)
              for div in soup.find_all("div", class_="editable-paragraph")
          ]
  
  def find_matches(paragraphs, word):
      matches = []
      for para in paragraphs:
          if word.lower() in para.lower():
              # Extract small snippet
              index = para.lower().find(word.lower())
              words = para[index:].split()
              snippet = " ".join(words[:context_words])
              matches.append(snippet)
      return matches
  
  lines_found = {}
  # Walk all files and search
  for root, _, files in os.walk(path):
      for file in files:
          if file.endswith(".html"):
              full_path = os.path.join(root, file)
              paragraphs = extract_paragraphs(full_path)
              snippets = find_matches(paragraphs, search_word)
              for s in snippets:
                links = full_path
                line = s
                if links not in lines_found:
                  lines_found[links] = []
                lines_found[links].append(line)
  
  return lines_found