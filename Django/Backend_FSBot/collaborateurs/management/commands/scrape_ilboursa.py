import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrapes data from ilboursa.com'

    def handle(self, *args, **options):
        url = 'https://www.ilboursa.com/'  # Adjust this to the actual URL if necessary
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scraping TUNINDEX
        tunindex = soup.find('a', text='TUNINDEX').parent.parent
        index_value = tunindex.find_next('span').text
        index_change = tunindex.find('span', class_='quote_up4').text if tunindex.find('span', class_='quote_up4') else "No change data"

        self.stdout.write(self.style.SUCCESS(f"TUNINDEX: {index_value}, Change: {index_change}"))

        # Scraping the highest rises
        hausses = soup.find('div', class_='bar121', text='+ FORTES HAUSSES').find_next('table')
        for row in hausses.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                symbol = cells[0].find('a').text
                value = cells[1].text
                change = cells[2].text
                self.stdout.write(self.style.SUCCESS(f"Hausses: {symbol} {value} {change}"))

        # Scraping the biggest falls
        baisses = soup.find('div', class_='bar121', text='+ FORTES BAISSES').find_next('table')
        for row in baisses.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                symbol = cells[0].find('a').text
                value = cells[1].text
                change = cells[2].text
                self.stdout.write(self.style.SUCCESS(f"Baisses: {symbol} {value} {change}"))
