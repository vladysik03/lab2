import csv
import requests
from bs4 import BeautifulSoup

# для работы программы необходимо установить библиотеки requests и bs4

# жанры, студии, многосерийность, рейтинг, завершенность
# ввод данных


count = 0
top_url = []
top_anime = []

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


def genres_checking(line, genre):
    genre_in_file = line[5]
    for i in range(len(genre)):
        if genre != "" and genre_in_file == "Unknown":
            return False
        elif str(genre[i]) not in genre_in_file:
            return False
    return True


def studios_checking(line, studio):
    studio_in_file = line[14]
    for i in range(len(studio)):
        if studio != "" and studio_in_file == "Unknown":
            return False
        elif studio[i] not in studio_in_file:
            return False
    return True


def seriality_checking(line, numberOfEpisodes):
    seriality_in_file = line[8]
    if numberOfEpisodes == "":
        return True
    elif seriality_in_file == "Unknown":
        return False
    elif numberOfEpisodes == "многосерийное" or numberOfEpisodes == "Многосерийное":
        if int(seriality_in_file) > 1:
            return True
        else:
            return False
    elif numberOfEpisodes == "полнометражное" or numberOfEpisodes == "Полнометражное":
        if int(seriality_in_file) == 1:
            return True
        else:
            return False


def rating_checking(line, ratingMin, ratingMax):
    rating_in_file = line[3]
    if ratingMin == "" and ratingMax == "":
        return True
    elif (ratingMin != "" or ratingMax != "") and rating_in_file == "Unknown":
        return False
    elif ratingMin != "" and ratingMax == "" and float(ratingMin) < float(rating_in_file):
        return True
    elif ratingMin == "" and ratingMax != "" and float(ratingMax) > float(rating_in_file):
        return True
    elif ratingMin != "" and ratingMax != "" and float(ratingMin) < float(rating_in_file) < float(ratingMax):
        return True
    else:
        return False


def completeness_cheking(line, completeness):
    completenes_in_file = line[9]
    if completeness == "":
        return True
    elif (completeness == "Да" or completeness == "да") and completenes_in_file == "True":
        return True
    elif (completeness == "Нет" or completeness == "нет") and completenes_in_file == "False":
        return True
    else:
        return False


result = open("result.txt", "w", encoding="utf-8")
with open("anime.csv", encoding="UTF-8") as file:
    reader = csv.reader(file)
    for index, line in enumerate(reader):
        if index != 0:
            filter = {genres_checking(line, genre), studios_checking(line, studio),seriality_checking(line, numberOfEpisodes),
                      rating_checking(line, ratingMin, ratingMax), completeness_cheking(line, completeness)}
            if all(filter):
                result.write(line[1] + '\n')
                if len(top_url) < 5:
                    top_url.append(line[16])
                    top_anime.append(line[1])
            count += 1
            print(line[1], count)
print(top_url)
result.close()

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "accept": "*/*"}
URL = ""


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.findAll("div", class_="mainEntry")
    for item in items:
        link = item.find("img", class_="screenshots").get("src")
        return link


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print("Error")


for position in range(len(top_url)):
    img = requests.get("https://www.anime-planet.com" + parse(top_url[position]))
    if img.status_code == 200:
        img_option = open(top_anime[position] + ".jpg", "wb")
        img_option.write(img.content)
        img_option.close()
