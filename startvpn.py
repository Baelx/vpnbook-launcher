#!/usr/bin/python3

from PIL import Image
import pyperclip, pytesseract, requests, bs4, re, subprocess, pexpect, sys, os

print("Fetching fresh credentials from vpnbook...)
try:
    res = requests.get('https://vpnbook.com/freevpn')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    passwd_img = soup.select('html body div#main article#pricing div.container div.one-third.column.box.light.featured ul.disc li img')

    match_img_src = re.compile(r'\"(.*?)\"')
    img_pass_src = match_img_src.search(str(passwd_img))
    new_pic = requests.get('https://vpnbook.com/' + img_pass_src.group(1))
    open('password.png', 'wb').write(new_pic.content)
    print('SUCCESS')
except IOError:
    print("WARNING: Couldn't reach vpnbook server.\nWill try to authenticate with existing password if it's found in the current directory.")

print('Scanning image for password...)
try:
    im = Image.open('password.png')
    password_text = pytesseract.image_to_string(im)
    print('SUCCESS')
except IOError:
    print("ERROR: No password image found in current directory. Can't connect without password.\nExiting.")

subprocess.call(['sudo', '/usr/sbin/openvpn', '--config', 'vpnbook-us1-tcp80.ovpn'])

#child = pexpect.spawn('sudo /usr/sbin/openvpn --config vpnbook-us1-tcp80.opvn')
#child.expect('Enter Auth Username:')
#child.sendline('testing')
