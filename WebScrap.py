import browserhistory as bh
import sqlite3
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import socket

# """         Storing the browser history in a .csv file          """
#
# con = sqlite3.connect('C:\\Users\\chintu\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
# c = con.cursor()
#
# columns = [["URL", "Title", "Visit Count", "Last Visit Time"]]
# c.execute("select url, title, visit_count, last_visit_time from urls") #urls,keyword_search_terms
# results = c.fetchall()
#
# c.close()
#
# file = open('history.csv', 'w+', encoding='utf-8', newline='')
# with file:
#     write = csv.writer(file)
#     write.writerows(columns)
#
# for r in results:
#     r = list(r)
#     for i in range(len(r)):
#         if isinstance(r[i], int):
#             r[i] = str(r[i])
#
# file = open('history.csv', 'a+', encoding='utf-8', newline='')
# with file:
#     write = csv.writer(file)
#     write.writerows(results)
#
# """         This code needs to be run just once to get the Browser History File          """

#########################################################################

"""         Blacklisting part           """

def clean_url(s):
    x = s.find("/")
    s = s[x+2:s.find("/", x+2)]
    return s

blacklisting = open('blacklist.csv', 'r', encoding='utf-8', newline='')
blacklist = []
data = pd.read_csv('history.csv',encoding='utf-8')
columns = ["URL", "Title"]
weird=[]
count = 0

for i in blacklisting:
    blacklist.append(i[:-2])

for i in data["Title"]:
    for b in blacklist:
        if isinstance(i,int)==False and isinstance(i,float)==False and  b in i:
            x=[b]
            data["URL"][count] = clean_url(data["URL"][count])
            for c in columns:
                x.append(data[c][count])
            weird.append(x)
    count+=1

columns.insert(0, "Keywords")
file = open('weird.csv', 'w+', encoding='utf-8', newline='')
with file:
    write = csv.writer(file)
    write.writerows([columns])
    write.writerows(weird)

# print("Your results are stored in weird.csv")

##############################################

"""         Web Scraping        """

# getting IP address
def getIP(domain):
    url = "https://domainbigdata.com/"
    page = urllib.request.Request(url+domain, headers={'User-Agent': 'Mozilla/5.0'})
    infile = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(infile, features="html.parser")
    try:
        section = soup.find("tr", {"id":"trIP"})
        anchor = section.find("a")
        ip = anchor.get("href")[1:]
        getGeo(ip)
    except:
        try:
            getGeo(domain)
        except:
            print()

# getting geographic details
def getGeo(ip):
    parameters = {"ip": ip}
    response = requests.post("https://www.ipaddress.my/", data = parameters)
    soup = BeautifulSoup(response.text, 'html.parser')

    res = {"Hostname:":"","Domain Name:":"","ISP:":"","City:":"","Country:":"","Latitude:":"","Longitude:":"","ZIP Code:":"","Area Code:":""}

    for i in res:
        res[i] = soup.find("td", text=i).find_next_sibling("td",text=True)
        if res[i]!=None:
            res[i] = res[i].get_text()

    res["Domain Name:"] = soup.find("td", text="Domain Name:").find_next().findChild("a")
    if res["Domain Name:"]!=None:
        res["Domain Name:"] = res["Domain Name:"].get_text()

    r = []
    for i in res:
        r.append([i,res[i]])
    r.append(["IP Address:",ip])
    write_to_file(r,ip)

def write_to_file(r,ip):
    file = open('results.csv', 'a+', encoding='utf-8', newline='')
    with file:
        write = csv.writer(file)
        write.writerows([[ip],[""]])
        write.writerows(r)
        write.writerows([[""], [""]])

store = open('results.csv', 'w+', encoding='utf-8', newline='')
domains = set()
with open('weird.csv', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for i in csv_reader:
        if i[1]=="URL":
            continue
        domains.add(i[1])

url = list(domains)

for i in url:
    getIP(i)
print("Results stored in results.csv")


"""             Blocking the flagged websites           """

# Get the list of domains to be blocked

"""
# Initialization
i=0
iplist=[]
blacklist=[]
# Read the blacklist csv file and gets the IPs
with open('results.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        i = i + 1
        if i%14 == 1:
            iplist.append(row)
# Gets the url from the IP address using reverse DNS lookup
for ip in iplist:
#    print(ip)
    try:
        url = socket.gethostbyaddr(ip[0])
        blacklist.append(url[0])
    except:
        print("URL not found")
#    print(url[0])
#    blacklist.append(url[0])
"""



# Path to the system blacklist file

filepath = "C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
blacklist = url
#Adding the URLs obtained to the system blacklist
with open(filepath, 'a') as file:
    for url in blacklist:
        file.write(redirect+" "+url+"\n")

# The sites in the blacklist should be blocked now