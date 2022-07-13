import requests
from bs4 import BeautifulSoup
from datetime import date
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', nargs='?', default='de', help='language to translate to (e.g \"en\")', type=str)
parser.add_argument('-d', '--date', nargs='?', default='today', help='specify a specific date to retrieve the menu plan for (in format YYYY-MM-DD)', type=str)
parser.add_argument('-m', '--mensa', nargs='?', default='Mensa Arcisstraße', help='choose the mensa to retrieve the menu plan for (e.g. \"Mensa Arcisstraße\"', type=str)
args = parser.parse_args()
  
# Returns the current local date
if args.date == 'today':
    date = date.today()
else:
    date = date.fromisoformat(args.date)

# check if today is a weekday
if date.weekday() >= 5:
    if args.date == 'today':
        print('Today is not a weekday. The mensa is not open today.')
    else:
        print('The specified day is not a weekday. The mensa is not open on that day.')
    sys.exit()

# definitions
mensa_dict = {'Mensa Arcisstraße': 421, 'Mensa Leopoldstraße': 411, 'Mensa Garching': 422}
url = f'https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_{str(date)}_{mensa_dict[args.mensa]}_-de.html'

# do HTML request and create BeautifulSoup object
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')

# gather data belonging to classes of interest
dish_descriptions = soup.find_all(class_='js-schedule-dish-description')
artnames = soup.find_all(class_='stwm-artname')

# print out the mensa menu
print(f'Speiseplan {args.mensa} am {str(date)}:\n')
for i, (dish_description, artname) in enumerate(zip(dish_descriptions, artnames)):

    # if artname is not there then just print an empty string instead
    if len(artname) > 0:
        print('{:<15} {:<1}'.format(artname.contents[0], dish_description.contents[0]))
    else:
        print('{:<15} {:<1}'.format('', dish_description.contents[0]))