import mechanize
from bs4 import BeautifulSoup 
import csv


class webScraping():

    print("START....")

    def start_scrapig(self):

        regiao = input("INFORME O ESTADO (EXP.: PI/SP): ").lower()
        url = "https://pi.olx.com.br/imoveis?f=p&sf=1&o=1" 

        browser = self.create_browser()
        #auth = self.authentication(browser)
        html = self.request(browser, url)
        anuncios = self.get_anuncios(html, regiao)
        #anunciante = self.get_anunciante(anuncios)

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
               if produto.a and str(produto.a).find(regiao) >= 0 and str(produto.a).find("?f=p") < 0:
                   anuncios += [produto.a.get('href')]

        print(anuncios, len(anuncios))
        return anuncios

    def get_anunciante(self, anuncios):

        for anuncio in anuncios:

            html = self.req_browser(anuncio)
            soup = BeautifulSoup(html, 'html.parser')

    def save_file(self):

        fieldnames = ['name', 'telefone']

        rows = [
            {'name': 'Albania', 'telefone': 28748},
            {'name': 'Algeria', 'telefone': 2381741},
            {'name': 'American Samoa', 'telefone': 199}
        ]

        with open('anuncios.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == '__main__':

   web = webScraping() 
   web.start_scrapig()
