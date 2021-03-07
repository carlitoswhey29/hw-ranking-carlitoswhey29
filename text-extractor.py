
import sys
import os
import subprocess as sub
import re
from boilerpipe.extract import Extractor

def validate_string(txt):
    string_encode = txt.encode("utf-8", "ignore")
    string_decode = string_encode.decode()
    return (string_decode)

def main(args=None):
  MAX_COUNT = 939
  counter = 0
  directory = r'./pages/'
  new_dir = './html/'
  old_dir = './pages/'
  other_dir = './extracted/'
  for filename in os.listdir(directory):
    new_name =  filename.replace('.txt', '.html')
    old_location = old_dir  + filename
    new_location = new_dir + new_name
    other_location = other_dir + new_name
    sub.run(['cp', old_location, new_location])
    extracted_data =''

    with open(new_location, 'r') as file_data:
      try:
        decoded_text = file_data.read()
        # decoded_text = validate_string(file_data.read())
        extractor = Extractor(extractor='ArticleExtractor', html=decoded_text)
        extracted_data = extractor.getText()
      except Exception as e:
          print(type(e))
          continue
    
    with open(other_location, 'w') as f:
      print (extracted_data, file=f)

    counter = counter + 1
    if counter > MAX_COUNT: break

if __name__ == "__main__":
    main()