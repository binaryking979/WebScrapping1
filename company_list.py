from selenium.webdriver.common.by import By
import time
from seleniumbase import Driver
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = Driver(uc=True)
driver.maximize_window()
url = 'https://ranking-empresas.eleconomista.es/ranking_empresas_nacional.html?qProvNorm=ALAVA'
driver.get(url)
time.sleep(3)
cookieBtn = driver.find_element(By.ID, 'didomi-notice-agree-button')
cookieBtn.click()
time.sleep(2)

category_options = driver.find_elements(By.CSS_SELECTOR, '#sel_sect_rankings>option')
option_length = len(category_options)
category_ids = []
for i in range(1,option_length):
    category_id = (category_options[i].text).split("-")[0]
    print(category_id)
    category_ids.append(category_id)

# -----------------------------------------------------------------------------------------------------------
company_name_header = ['national_position', 'position_evolution','company_name','billing', 'category','company_link']
csv_file = 'company_name_list.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as data_file:
    writer = csv.writer(data_file)
    writer.writerow(company_name_header)
#-------------------------------------------------------------------------------------------------------------

prev_height = -1
max_scrolls = 100
scroll_count = 0
#---------------------
# flag = True
company_lists_for_search = []
for i in range(38):
    print(f'-------------------{i}---------------------')
    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # give some time for new results to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height
        scroll_count += 1

    national_positions = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[1]')
    position_evolutions = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[2]')
    company_links = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[3]/a')
    billings = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[4]')
    categories = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[5]')
    length = len(national_positions)
    print("length:", length)
    company_lists = []

    for j in range(length):
         
     
        national_position = national_positions[j].text
        position_evolution = position_evolutions[j].text
        company_name = company_links[j].text
        billing = billings[j].text
        category = categories[j].text
        company_link = company_links[j].get_attribute('href')
        company_list = [national_position, position_evolution, company_name, billing, category,company_link]
        company_list_for_search = [category, company_link]
        company_lists_for_search.append(company_list_for_search)
        company_lists.append(company_list)

    csv_file = 'company_name_list.csv'
    with open(csv_file, 'a', newline='', encoding='utf-8') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(company_lists)
    nextButt = driver.find_element(By.CSS_SELECTOR, '#tabla-ranking > div:nth-child(8) > ul > li:last-child')
    nextButt.click()
    time.sleep(3)