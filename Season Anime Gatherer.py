
from bs4 import BeautifulSoup
import os
import requests

# pre-req or common


def get_html_text_main_page():
    url = "https://myanimelist.net/anime/season"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup


def path_maker():
    code = get_html_text_main_page()
    url = "https://myanimelist.net/anime/season"
    season = ""
    season = code.find('a',{"class":"on"}).get_text()
    while ('\n' or '  ') in season:
        season = season.replace('\n','')
        season = season.replace('  ','')

    path = "Seasonal Anime Data\\" + season + "\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


path = path_maker()


def code_to_links_main(code):
    link_list = []
    code = code.find("div", {"class": "seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix"})
    for x in code.findAll("div", {"class": "seasonal-anime js-seasonal-anime"}):
        y = x.find("a", {"class": "link-title"})
        link = y.get('href')
        link = str(link)
        link_list.append(link)

    return link_list


def get_html_text_se_page(links):
    source_codes = []
    driver = webdriver.Chrome()
    for link in links:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        source_codes.append(soup)
    driver.quit()
    return source_codes


def code_to_info_get(code):
    for x in code.findAll("div", {"class": "spaceit"}):
        text = x.get_text()
        print(text + "\n")


# part 1 list generator

def get_names_fast(code):
    file = open(path + "Data list.txt", "w", encoding="utf-8")
    tv_series = code.find("div", {"class": "seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix"})
    index = 1
    for x in tv_series.findAll("div", {"class": "seasonal-anime js-seasonal-anime"}):
        y = x.find("a", {"class": "link-title"})
        text = y.get_text()
        try:
            file.write(text + "\n")
        except UnicodeEncodeError:
            print("Unable to write the title ' " + text +" 'due to Unicode Error at line no " + str(index))
            file.write("UnicodeEncodeError: UNABLE TO DECODE NAME\n")
        index += 1




# part 2 data gatherer


def get_names_fast_2(code):
    file = open(path + "Data complete.txt", "w", encoding="utf-8")
    tv_series = code.find("div", {"class": "seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix"})
    for x in tv_series.findAll("div", {"class": "seasonal-anime js-seasonal-anime"}):


        title = x.find("a", {"class": "link-title"}).get_text()
        try:
            file.write(("Name : " + title + "\n"))
        except UnicodeEncodeError:
            file.write("UnicodeEncodeError: UNABLE TO DECODE NAME:\n")
            print("Unable to write the title ' " + title +" 'due to Unicode Error")


        file.write("Genres : ")
        genres = x.findAll("span", {"class": "genre"})
        for genre in genres:
            file.write( genre.find("a", {}).get_text() + ", ")


        source = x.find("span", {"class": "source"})
        file.write("\nSource : " + source.get_text())


        date = x.find("span", {"class": "remain-time"}).get_text()
        while True:
            if "  " in date or "\n" in date:
                date = date.replace("  ","")
                date = date.replace("\n","")
            else:
                break
        file.write("\nRelease date : " + date)


        rating = x.find("span", {"class": "score"}).get_text()
        while True:
            if "  " in rating or "\n" in rating:
                rating = rating.replace("  ","")
                rating = rating.replace("\n","")
            else:
                break
        file.write("\nRating : " + rating)


        
        file.write("\nSynopsis : \n")
        synopsis = x.find("span", {"class","preline"})
        text_synopsis = synopsis.get_text()

        synopsis_pieces = text_synopsis.split(" ")

        file.write("\n      ")

        length1 = 0
        for synopsis_piece in synopsis_pieces:
            length2 = len(synopsis_piece)
            length1 += length2
            if length1 < 150:
                file.write(synopsis_piece + " ")
            else:
                file.write("\n" + synopsis_piece + " ")
                length1 = 0
            length1 +=1



        file.write("\n\n-----------------------------------end-----------------------------------\n\n\n\n\n")


get_names_fast(get_html_text_main_page())
get_names_fast_2(get_html_text_main_page())

print("Data saved at '"+ path_maker() + "'")
input("Process Complete... Press enter to continue")

        

