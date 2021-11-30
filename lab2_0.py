import csv
import requests
from bs4 import BeautifulSoup

# для работы программы необходимо установить библиотеки requests и bs4

# жанры, студии, многосерийность, рейтинг, завершенность
# ввод данных


print("Какой жанр вас интересует?")
genre = str(input())
genre = genre.split(",")
print("Вас интересует многосерийное аниме или полнометражное?")
numberOfEpisodes = str(input())
print("Какая студия вас интересует?")
studio = str(input())
studio = studio.split(",")
print("Какой рейтинг вас интересует?\nОт:")
ratingMin = str(input())
print("До:")
ratingMax = str(input())
print("Вас интересуют завершенные аниме? (Да\Нет)")
completeness = str(input())


def genres(line, genre):
    for i in range(len(genre)):
        if genre == '':
            return True
        elif genre != '' and line[5] == 'Unknown':
            return False
        elif str(genre[i]) not in line[5]:
            return False
        elif i == len(genre) - 1:
            return True


def studios(line, studio):
    for i in range(len(studio)):
        if studio == '':
            return True
        elif studio != '' and line[14] == 'Unknown':
            return False
        elif studio[i] not in line[14]:
            return False
        elif i == len(studio) - 1:
            return True


def seriality(line, numberOfEpisodes):
    if numberOfEpisodes == '':
        return True
    elif numberOfEpisodes != '' and line[8] == 'Unknown':
        return False
    elif numberOfEpisodes == "многосерийное" or numberOfEpisodes == "Многосерийное":
        if int(line[8]) > 1:
            return True
        else:
            return False
    elif numberOfEpisodes == "полнометражное" or numberOfEpisodes == "Полнометражное":
        if int(line[8]) == 1:
            return True
        else:
            return False


def rating(line, ratingMin, ratingMax):
    if ratingMin == '' and ratingMax == '':
        return True
    elif (ratingMin != '' or ratingMax != '') and line[3] == 'Unknown':
        return False
    elif ratingMin != '' and ratingMax == '' and float(ratingMin) < float(line[3]):
        return True
    elif ratingMin == '' and ratingMax != '' and float(ratingMax) > float(line[3]):
        return  True
    elif ratingMin != '' and ratingMax != '' and float(ratingMin) < float(line[3]) < float(ratingMax):
        return True
    else:
        return False


def completenessCheck(line, completeness):
    if completeness == '':
        return True
    elif (completeness == 'Да' or completeness == 'да') and line[9] == 'True':
        return True
    elif (completeness == 'Нет' or completeness == 'нет') and line[9] == 'False':
        return True
    else:
        return False


count = 0
result = open("result.txt", "w", encoding='utf-8')
top_url = []
top_anime = []
with open("anime.csv", encoding="UTF-8") as file:
    reader = csv.reader(file)
    for index, line in enumerate(reader):
        if index != 0:
            if genres(line, genre) and studios(line, studio) and seriality(line, numberOfEpisodes)\
                    and rating(line, ratingMin, ratingMax) and completenessCheck(line,completeness):
                result.write(line[1]+'\n')
                if len(top_url) < 5:
                    top_url.append(line[16])
                    top_anime.append(line[1])
            count += 1
            print(line[1], count)
print(top_url)
result.close()
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36','accept':'*/*'}
URL = ''


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='mainEntry')
    for item in items:
        link = item.find('img', class_='screenshots').get('src')
        return link


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print("Error")


for position in range(len(top_url)):
    img = requests.get('https://www.anime-planet.com'+parse(top_url[position]))
    if img.status_code == 200:
        img_option = open(top_anime[position] + '.jpg', 'wb')
        img_option.write(img.content)
        img_option.close()
