#!/usr/bin/python3

from PIL import Image
import pyperclip, pytesseract, requests, bs4, re, subprocess

print("Fetching credentials...")
try:
    res = requests.get('https://vpnbook.com/freevpn')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    passwd_img = soup.select('html body div#main article#pricing div.container div.one-third.column.box.light.featured ul.disc li img')

    match_img_src = re.compile(r'\"(.*?)\"')
    img_pass_src = match_img_src.search(str(passwd_img))
    new_pic = requests.get('https://vpnbook.com/' + img_pass_src.group(1))
    open('password.png', 'wb').write(new_pic.content)

except IOError:
    print("WARNING: Couldn't reach vpnbook server. Will try to authenticate with existing password if it's found in the current directory.")

try:
    im = Image.open('password.png')
    text = pytesseract.image_to_string(im)
    print(text)
except IOError:
    print("ERROR: No password image found in current directory. Can't connect without password. Exiting.")

subprocess.call(['sudo', '/usr/sbin/openvpn', '--config', 'vpnbook-us1-tcp80.ovpn'])


