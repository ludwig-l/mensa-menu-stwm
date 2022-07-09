import requests
from bs4 import BeautifulSoup


# definitions
date = '2022-07-08'
mensa_dict = {'Mensa Arcisstraße': 421, 'Mensa Leopoldstraße': 411, 'Mensa Garching': 422}
mensa_name = 'Mensa Arcisstraße'
url = f'https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_{date}_{mensa_dict[mensa_name]}_-de.html'

# do HTML request and create BeautifulSoup object
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')

# gather data belonging to classes of interest
dish_descriptions = soup.find_all(class_='js-schedule-dish-description')
artnames = soup.find_all(class_='stwm-artname')

# print out the mensa menu
print(f'Speiseplan {mensa_name} am {date}:\n')
for i, dish_description in enumerate(dish_descriptions):

    # if artname is not there then just print an empty string instead
    if len(artnames[i]) > 0:
        print('{:<15} {:<1}'.format(artnames[i].contents[0], dish_description.contents[0]))
    else:
        print('{:<15} {:<1}'.format('', dish_description.contents[0]))