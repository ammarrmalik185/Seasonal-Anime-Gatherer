from selenium import webdriver
import xlsxwriter
import time

driver = webdriver.Chrome()
driver.get("https://myanimelist.net/anime/season")


# start_date
# sort


def change_sort():
    driver.find_element_by_class_name("sort").click()
    driver.find_element_by_id("start_date").click()
    time.sleep(1)
    driver.get("https://myanimelist.net/anime/season")


seasonal_anime_list_container = driver.find_element_by_class_name("js-seasonal-anime-list-key-1")
seasonal_animes = seasonal_anime_list_container.find_elements_by_class_name("seasonal-anime")

title = seasonal_animes[0].find_element_by_class_name("link-title").text
link = seasonal_animes[0].find_element_by_class_name("link-title").get_attribute("href")
genres = seasonal_animes[0].find_elements_by_class_name("genre")
synopsis = seasonal_animes[0].find_element_by_class_name("preline").text
release = seasonal_animes[0].find_element_by_class_name("remain-time").text




































