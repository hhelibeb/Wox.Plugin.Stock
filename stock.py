from util import WoxEx, WoxAPI, load_module, Log

with load_module():
    from bs4 import BeautifulSoup
    import requests
    import webbrowser
    import urllib
    import shutil
    import json
    from os import path

LIST_KEYWORDS = ['-ALL', '-all']


class Main(WoxEx):

    def query(self, param):

        q = param.strip()
        if not q:
            return

        results = []

        if q in LIST_KEYWORDS:
            if not path.exists("list.json"):
                shutil.copyfile('list_template.json', 'list.json')
            try:
                with open('list.json', 'r', encoding='utf-8') as f:
                    stocks = json.load(f)
                    if stocks:
                        for item in stocks:
                            results += [self.get_stock(keyword=item['name'])]
            except (IOError, ValueError) as e:
                return
            return results

        result = self.get_stock(keyword=q)
        results += [result]

        return results

    def open_url(self, url=None):
        webbrowser.open(url)

    def get_stock(self, keyword=None):

        url = f'https://www.google.com/search?q={keyword} stock'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                   'Connection': 'close'}
        # proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        proxies = urllib.request.getproxies()
        r = requests.get(url, headers=headers, proxies=proxies)
        r.close()

        soup = BeautifulSoup(r.text, 'html.parser')

        name_div = soup.find('div', class_='oPhL2e')
        if not name_div:
            return
        name = name_div.string

        price = ''
        price_div = soup.find('span', jsname='vWLAgc')
        if price_div:
            price = price_div.string

        code = soup.find('div', class_='HfMth').string

        currency = ''
        currency_div = soup.find('span', jsname='T3Us2d')
        if currency_div:
            currency = currency_div.string

        change_percent = soup.find('span', jsname='qRSVye').string
        change_numeric = soup.find('span', jsname='rfaVEf').string

        blank = '      '
        result = {
            'Title': name,
            'SubTitle': code + blank + price + ' ' + currency + blank + change_percent + ' ' + change_numeric,
            'IcoPath': 'img\\stock.ico',
            'JsonRPCAction': {
                'method': 'open_url',
                'parameters': [url]
            }
        }

        return result


if __name__ == '__main__':
    Main()
