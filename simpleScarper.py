'''
Simple web scarper 
@uthor: LTIFI Azer, AzsezA
'''
import requests
import urllib.request
from bs4 import BeautifulSoup
import wget
#import re
import csv
site= ''#URL Of the site

#Testing the links if they are downloadble 
def isDow(url:str):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if content_type == None :
        return True
    elif 'text' in content_type.lower():
        return False
    else :
        return True
#Begin
print('requesting : '+site +' ...')

resp = requests.get(site)
soup = BeautifulSoup(resp.text, 'html')

print('prasing all links')

allA = soup.find_all('a', string=True)
print('printing output in links.csv ...' )
with open('links.csv', 'w', newline='') as csvfile:
    header = ['Dirty link','Clean link','Is it Downloadble']
    writer = csv.DictWriter(csvfile,fieldnames = header)
    writer.writeheader()
    for link in allA:
        a = link.get('href')
        print('Testing :  '+a)
        b = ''+link.get('href')#put the domain name in the first part 
        if type(b) != None:
            print(type(b))
            print('link'+a)
            c = isDow(b)
        else :
            c = None
        writer.writerow({'Dirty link': a,
            'Clean link': b,
            'Is it Downloadble': c})
print("done")import sys
import urllib.request
print("opening CSV file")
#opening links.csv to extract the good links
i = 1
with open('links.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    print("done opening the file")
    for row in reader :
        if row['Is it Downloadble'] == 'True' :
            print("downloading file  "+str(i)+" : "+row['Dirty link'])
            urllib.request.urlretrieve(row['Clean link'])
            print("Done !! ")
            i+=1

