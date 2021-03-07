
import sys
import os
import subprocess as sub
import re


def convert_to_title(txt):
  for punc in ['/','=','?','+','.','&','%']:
    if punc in txt:
      txt = txt.replace(punc, '_')
  http_list = re.split("__", txt)
  if len(http_list) < 3:
    x = str(http_list[1])
  else:
    x = str(http_list[2])
  return x

def download_link_content(name, link):
  p1 = sub.run(['wget', '--limit-rate=1m','--tries=2', '-O', name, link], stdout=sub.PIPE, text=True)
  with open('./logs/errors.txt', 'a+') as f:
    if p1.returncode != 0 and p1.stderr != None :
      print (p1.stderr, file=f)

def my_progress(count):
  total = 1000
  p = count / total
  if p > 0 and p % 1 == 0 :
    print ('*', end='')

def main(args=None):
  MAX_COUNT = 999
  counter = 0
  file_name = "./links.txt"

  with open(file_name, 'r') as links:
    for link in links:
      new_name = './pages/' + str(convert_to_title(link)).rstrip() + '.txt'
      active_link = str(link).rstrip()
      download_link_content(new_name, active_link)
      counter = counter + 1
      my_progress(counter)
      if counter > MAX_COUNT: break

if __name__ == "__main__":
    main()