import mechanize
from bs4 import BeautifulSoup 
import csv
import json


class webScraping():

    def start_scrapig(self):

        regiao = input("INFORME O ESTADO (EXP.: PI/SP): ").lower()

        pags = 3

        while pags > 0:
            pags -= 1

        url = f"https://{regiao}.olx.com.br/imoveis?f=p&sf=1&o=1" 

        browser = self.create_browser()
        html = self.request(browser, url)
        anuncios = self.get_anuncios(html, regiao)
        anunciante = self.get_anunciante(browser, anuncios)
        self.save_file(anunciante)

        print("Finalizado...")

    def create_browser(self):

        br = mechanize.Browser()

        br.set_handle_equiv(True)
        br.set_handle_gzip(False)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
            U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
            Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        return br

    def authentication(self, browser):

        url = "https://conta.olx.com.br/"
        browser.open(url)

        for forms in browser.forms():
            print(forms)

        browser.form['email'] = email
        browser.form['password'] = senha

        browser.submit()

    def request(self, browser, url):

        browser.open(url)
        html = browser.response().read()

        return html

    def get_anuncios(self, html, regiao):

        soup = BeautifulSoup(html, 'html.parser')
        all_ul = soup.find_all('ul')

        anuncios = []
        for ul in all_ul:
           produtos = ul.find_all('li') 

           for produto in produtos:
               if produto.a and str(produto.a).find(f"https://{regiao}.olx.com.br/") >= 0 and str(produto.a).find("?f=p") < 0:
                   anuncios += [produto.a.get('href')]

        return anuncios

    def get_anunciante(self, browser, anuncios):

        props = []
        for index, anuncio in enumerate(anuncios):
            print(f"{index} de {len(anuncios)}...")

            html = self.request(browser, anuncio)
            soup = BeautifulSoup(html, 'html.parser')
            scripts = soup.find_all('script')

            for data in scripts:
                if str(data).find('data-json') >= 0:

                    try:
                        data = data.attrs
                        user = json.loads(data['data-json'])['ad']['user']['name']
                        phone = json.loads(data['data-json'])['ad']['phone']['phone'] 

                        props += [{'name': user, 'telefone': phone if phone else ""}]

                    except:
                        pass

        return props

    def save_file(self, data):

        fieldnames = ['name', 'telefone']

        rows = data 

        with open('anuncios.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == '__main__':

   web = webScraping() 
   web.start_scrapig()
