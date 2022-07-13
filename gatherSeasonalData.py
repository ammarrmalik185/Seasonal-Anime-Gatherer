from selenium import webdriver
import xlsxwriter
import time
import os


class Options:
    def __init__(self, logs=False, silent=False, save_path="Seasonal Anime Data", timeout=30, season="current",
                 sort="start_date"):
        self.logs = logs
        self.silent = silent
        self.save_path = save_path
        self.timeout = timeout
        self.season = season
        self.sort = sort


class AnimeDataGatherer:

    def __init__(self, option=Options()):
        self.url = None
        self.data = []
        self.currentSeason = "unknown"
        self.options = option
        self.driver_options = webdriver.ChromeOptions()
        self.driver_options = webdriver.IeOptions()
        if not self.options.logs:
            self.driver_options.add_argument('log-level=3')
        if self.options.silent:
            self.driver_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(options=self.driver_options)
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Edge()
        self.driver.set_page_load_timeout(self.options.timeout)
        
    def get_season_page(self):
        if self.options.season == "current":
            self.url = "https://myanimelist.net/anime/season"
        else:
            self.url = "https://myanimelist.net/anime/season/" + self.options.season
        self.driver.get(self.url)
        
    def set_sort(self):
        js = "let aa=document.getElementsByClassName('modal-container')[0];aa?.parentNode?.removeChild(aa)"
        self.driver.execute_script(js)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_class_name("sort"))
        #self.driver.find_element_by_class_name("sort").click()
        self.driver.find_element_by_id(self.options.sort).click()
        time.sleep(1)
        self.driver.get(self.url)

    def gather_data(self):

        self.currentSeason = self.driver.find_element_by_class_name("on").text

        seasonal_anime_list_container = self.driver.find_element_by_class_name("js-seasonal-anime-list-key-1")
        seasonal_animes = seasonal_anime_list_container.find_elements_by_class_name("seasonal-anime")
    
        for seasonal_anime in seasonal_animes:
            title = seasonal_anime.find_element_by_class_name("link-title").text
            if title == "":
                continue
            link = seasonal_anime.find_element_by_class_name("link-title").get_attribute("href")
            synopsis = seasonal_anime.find_element_by_class_name("preline").text
            date_full = seasonal_anime.find_element_by_class_name("prodsrc").find_element_by_class_name("info").find_element_by_class_name("item").text
            date = date_full.split(",")[0]
            genres_elements = seasonal_anime.find_elements_by_class_name("genre")
            genres = []
            genres_string = ""
            for genre_element in genres_elements:
                genre_text = genre_element.text
                genres.append(genre_text)
                genres_string += genre_text + ", "

            self.data.append({
                "title": title,
                "link": link,
                "synopsis": synopsis,
                "date": date,
                "date_full": date_full,
                "genres": genres,
                "genres_string": genres_string
            })
        self.driver.close()

    def write_to_file(self):
        parent_path = self.options.save_path + "\\" + self.currentSeason + "\\"
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        workbook = xlsxwriter.Workbook(parent_path + 'Data Sheet.xlsx')
        worksheet = workbook.add_worksheet()
        file_list = open(parent_path + "Data list.txt", "w", encoding="UTF-8")
        file_details = open(parent_path + "Data Complete.txt", "w", encoding="UTF-8")
    
        row = 2
        column = 2

        worksheet.write(row-1, column, "Title")
        worksheet.write(row-1, column + 1, "Date")
        worksheet.write(row-1, column + 2, "Date full")
        worksheet.write(row-1, column + 3, "Genres")
        worksheet.write(row-1, column + 4, "link")

        for single_anime_data in self.data:
            worksheet.write(row, column, single_anime_data["title"])
            worksheet.write(row, column + 1, single_anime_data["date"])
            worksheet.write(row, column + 2, single_anime_data["date_full"])
            worksheet.write(row, column + 3, single_anime_data["genres_string"])
            worksheet.write(row, column + 4, single_anime_data["link"])
    
            file_list.write(single_anime_data["title"] + "\n")
    
            file_details.write("Name : " + single_anime_data["title"] + "\n")
            file_details.write("Genres : " + single_anime_data["genres_string"] + "\n")
            file_details.write("Release Date : " + single_anime_data["date_full"] + "\n")
            file_details.write("More info : " + single_anime_data["link"] + "\n")
            file_details.write("Synopsis : \n" + single_anime_data["synopsis"] + "\n")
            file_details.write("-----------------------------------end-----------------------------------\n\n")
    
            row += 1
    
        file_details.close()
        file_list.close()
        workbook.close()
    

Gatherer = AnimeDataGatherer(option=Options())
Gatherer.get_season_page()
Gatherer.set_sort()
Gatherer.gather_data()
Gatherer.write_to_file()
input("Completed. Press enter to continue ...")
