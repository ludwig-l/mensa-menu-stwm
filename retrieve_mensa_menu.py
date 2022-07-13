import requests
from bs4 import BeautifulSoup
from datetime import date
import sys
import argparse
from googletrans import Translator


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

# create translator object
translator = None
if args.lang != 'de':
    translator = Translator()

# print out the mensa menu
title_str = f'Speiseplan {args.mensa} am {str(date)}:' 
# translate if specified language is other than German
if args.lang != 'de':
    print(translator.translate(title_str, src='de', dest=args.lang).text, '\n')
else:
    print(title_str, '\n')
for i, (dish_description, artname) in enumerate(zip(dish_descriptions, artnames)):

    # if artname is not there then just print an empty string instead
    # translate if specified language is other than German
    if len(artname) > 0:
        if args.lang == 'de':
            print('{:<15} {:<1}'.format(artname.contents[0], dish_description.contents[0]))
        else:
            artname_tl = translator.translate(artname.contents[0], src='de', dest=args.lang).text
            dish_description_tl = translator.translate(dish_description.contents[0], src='de', dest=args.lang).text
            print('{:<15} {:<1}'.format(artname_tl, dish_description_tl + ' (orig.: \"' + dish_description.contents[0] + '\b\")')) # backspace because there is a tailing whitespace at the end of each entry
    else:
        if args.lang == 'de':
            print('{:<15} {:<1}'.format('', dish_description.contents[0]))
        else:
            dish_description_tl = translator.translate(dish_description.contents[0], src='de', dest=args.lang).text
            print('{:<15} {:<1}'.format('', dish_description_tl + ' (orig.: \"' + dish_description.contents[0] + '\b\")')) # backspace because there is a tailing whitespace at the end of each entry