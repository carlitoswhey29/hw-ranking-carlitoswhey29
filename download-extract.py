
import sys
import os
import subprocess as sub
import re
from boilerpipe.extract import Extractor

def convert_to_title(txt):
  # replace unacceptable title characters
  for punc in ['/','=','?','+','.','&','%']:
    if punc in txt:
      txt = txt.replace(punc, '_')
  # return the title after the http://
  http_list = re.split("__", txt)
  if len(http_list) < 3:
    x = str(http_list[1])
  else:
    x = str(http_list[2])
  return x

def download_link_content(name, link):
  # download link, limit retries to 2 to eliminate failed links, output
  # if you would like to run silently without all the output add the -q flag
  p1 = sub.run(['wget', '--limit-rate=1m','--tries=2', '-O', name, link], stdout=sub.PIPE, text=True)
  with open('./logs/errors.txt', 'a+') as f:
    if p1.returncode != 0 and p1.stderr != None :
      print (p1.stderr, file=f)

def extract_text(filename):
    with open(filename, 'r') as file_data:
      # this will fail if it reads unicode 
      # use a try except with continue
      decoded_text = file_data.read()
      extractor = Extractor(extractor='ArticleExtractor', html=decoded_text)
      extracted_data = extractor.getText()

      # Write extracted text to a txt file
      new_location = filename.replace('.html', '.txt')
      with open(new_location, 'w') as f:
        print (extracted_data, file=f)

myfile = './links.txt'
with open(myfile, 'r') as links:
    for link in links:
      # rename file
      new_name = './selected/' + str(convert_to_title(link)).rstrip() + '.html'
      # remove hanging whitespace
      active_link = str(link).rstrip()
      # Download html document
      download_link_content(new_name, active_link)
      # Extract text from html document
      extract_text(new_name)  
