# eSenSei


# Intro

eSenSei is a Cyber Parental Control tool, that we developed as a part of the Gurugram Police Cyber Security Summer Internship 2020. 

The tool basically has two primary modules:

**Module 1: Reconnaissance and Blacklisting using OSINT Framework by Web Scraping**

This module mainly focuses on looking for suspicious websites being visited by the child, and sketchy keyword searches on safe platforms like Google. We will mainly be analysing the browser history for such information, and create a report consisting of all these details.

**Module 2: System Activity Information Gathering**

This module focuses on the keystrokes that the child uses, and looks out for fishy information that the child is typing. This would help when the child is using messaging applications like Facebook Messenger or Whatsapp Web, where we cannot find details of every message being sent in the browser history.  

# Libraries

There are some Libraries that you will need to Download:

For Module 1, we need the following Python libraries:
Sqlite3 - to read the history database of the browser
Pandas and Csv - to handle the csv data
Requests and Urllib- to send HTTP requests to OSINT webpages and retrieve information
BeautifulSoup - to perform web scraping

For Module 2, we need the following libraries:
Pynput.keyboard - for keylogging
Socket and Requests - to handle the IP
from requests import get
Pyscreenshot - to take the screenshots
Psutil - for process killing
Smtplib and Email - for sending the resulting files in an email to the parent
Os, Time, Ctypes and Platform - for assisting the rest of the modules

# Working

We first need to first download the 3 files in the main branch and place them in a folder in the child's system.  
Next we need to just run eSenSei.py as an administrator and the files will hide themselves. 
If the child types any words which are in the blacklist, the code runs and runs and the output is emailed to the parent.

# Output

When a blacklisted word is detected, the browser tab is first closed, screenshot is taken and keystrokes are sent to the parent's email id.
The browser history is parsed and detailed by including IPs and Geolocations of these sites and sent to the parent via email.
Apart from this, the blacklisted sites are added to the system browser blacklist, so the child can't open them ever again.
