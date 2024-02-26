from selenium.webdriver.common.by import By
import pandas as pd
import time
from seleniumbase import Driver
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = Driver(uc=True)
driver.maximize_window()
url = 'https://ranking-empresas.eleconomista.es/ranking_empresas_nacional.html?qProvNorm=ALAVA'
driver.get(url)
time.sleep(2)
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
# national_position,position_evolution,company_name,billing,category,company_link
# -----------------------------------------------------------------------------------------------------------
csv_file = 'company_details.csv'
company_details_header = ['category','national_position','position_evolution','company_name','billing','company_link','Denominación','Objeto Social','Domicilio Social', 'Localidad',  'Teléfono', 'Otros Teléfonos','Fax','Forma Jurídica', 'Página Web','Otras Webs','Marcas', 'Actividad']
with open(csv_file, 'w', newline='', encoding='utf-8') as data_file1: 
    writer = csv.writer(data_file1)  
    writer.writerow(company_details_header) 
#-------------------------------------------------------------------------------------------------------------

#---------------------
# flag = True
company_lists_for_search = []
company_list_for_search = []
cat_dic = {}
	
    # read CSV file 
try:
    results = pd.read_csv('company_name_list.csv', usecols=["national_position","position_evolution","company_name","billing","category","company_link"]) 
    company_lists_for_search = results.values.tolist()
    # print(csv_list[0][0])
    
     # print("all_lenth-------------------------------------",(company_lists_for_search))     
except FileNotFoundError:
    print("Error: 'company_name_list.csv' file not found.")
    cat_dic = {}
    

		# print("set_to_short_set :",set_to_short_set)
#-----------------------------------------------------------------------------------------------------------------------
all_length = len(company_lists_for_search)  #3727
# cat_len = option_length-1
print("--all length---", all_length)
start_num = 0
while start_num < option_length:
    # for i in range(all_length):
        # company_list_for_search = []
    for company_list_for_search in company_lists_for_search:

        company_details = []

        print("company_list_for search: -------------------", company_list_for_search[4])
        print("category_id---------------------------------;", category_ids[start_num])
        
        if int(company_list_for_search[4])==int(category_ids[start_num]):
            print(f'-----OKAY----{company_list_for_search[4]}-------')
            try:
                driver.get(company_list_for_search[5])
                time.sleep(3)
            except:    # selenium.common.exceptions.TimeoutException:
                print("e")    
            all_length = all_length-1
            names = driver.find_elements(By.XPATH, '//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr/td[1]')
            values = driver.find_elements(By.XPATH, '//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr/td[2]')
            name_list = []
            value_list = []
            # national_position,position_evolution,company_name,billing,category,company_link
            company_detail = {'category':company_list_for_search[4],'national_position':company_list_for_search[0],'position_evolution':company_list_for_search[1],'company_name':company_list_for_search[2],'billing':company_list_for_search[3],'company_link':company_list_for_search[5],'Denominación':'','Objeto Social':'','Domicilio Social':'', 'Localidad':'',  'Teléfono':'', 'Otros Teléfonos':'','Fax':'','Forma Jurídica':'', 'Página Web':'','Otras Webs':'','Marcas':'', 'Actividad':''}
                        
            for k in range(len(names)):
                name = names[k].text
                value = ''
                if name in company_details_header:
                   
                    value = driver.find_element(By.XPATH,f'//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr[{k+1}]/td[2]').text
                    company_detail.update({name:value})    
                    continue
            # print("Loop:",k)    
            for key,val in company_detail.items():
                company_details.append(val)

            # company_details.append(company_detail)     

            csv_file = 'company_details.csv'
            with open(csv_file, 'a', newline='', encoding='utf-8') as data_file1:
                writer = csv.writer(data_file1)
                writer.writerow(company_details)
            # company_lists_for_search.pop(i)
            company_lists_for_search.remove(company_list_for_search)    
        company_list_for_search = []    
    start_num = start_num+1        
# # for category_option in category_options:
# category_num = 0
# for category_num in range(2,3):#category_nums+1):
#     print(f'=================={category_num}=================')
#     driver.get(url)
#     time.sleep(3)
#     driver.find_element(By.CSS_SELECTOR,'#sel_sect_rankings').click()
#     time.sleep(1)
#     category_option = driver.find_element(By.CSS_SELECTOR, f'#sel_sect_rankings>option:nth-child({category_num+1})')
#     # //*[@id="sel_sect_rankings"]/option[2]
#     category = category_option.text
#     print(f'---------------------{category}--------------------------')
#     category_option.mouseup()
#     # part_name  = i.text
#     time.sleep(10)
#     # wait = WebDriverWait(driver, 10)
#     # athlete1 = wait.until(EC.visibility_of_element_located
#     national_positions = []
#     position_evolutions = []
#     company_links = []
#     national_positions = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[1]')
#     position_evolutions = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[2]')
#     company_links = driver.find_elements(By.XPATH,'//*[@id="tabla-ranking"]/table/tbody/tr/td[3]/a')
#     companys = []
#     for j in company_links:
#         companys.append(j.get_attribute('href'))
#     list_num = len(national_positions)
#     # com
#     # all_company_lists = {}
    
#     # print('len(j):', len(national_positions))
    
#     all_company_lists = []
#     for j in range(list_num-1):
#         print("j1:", j+1)
#         company_description = []
#         national_position = national_positions[j].text
#         position_evolution = position_evolutions[j].text
#         company_link = company_links[j].get_attribute('href')
#         company_name = company_links[j].text
#         company_description.append(category)
#         company_description.append(national_position)
#         company_description.append(position_evolution)
#         company_description.append(j+1)
#         company_description.append(company_name)
#         company_description.append(company_link)
#         print("Company_description:", company_description)
#         all_company_lists.append(company_description)

#     csv_file = 'company_name_list.csv'
#     with open(csv_file, 'a', newline='', encoding='utf-8') as data_file:
#         writer = csv.writer(data_file)
#         writer.writerows(all_company_lists)
#         # for item in all_company_lists:
#         #     writer.writerow([item])
  
#     #--------------------------------
#     company_details = []
#     for company in companys:
#         print('===================================================={part_name}=====================================================')
#         # company_link = company.get_attribute('href')
#         print('j2:', company)
#         driver.get(company)
#         time.sleep(2)
#         names = driver.find_elements(By.XPATH, '//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr/td[1]')
#         # values = driver.find_elements(By.XPATH, '//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr/td[2]')
#         name_list = []
#         value_list = []
#         company_detail = {'Denominación':'','Objeto Social':'','Domicilio Social':'', 'Localidad':'',  'Teléfono':'', 'Otros Teléfonos':'','Fax':'','Forma Jurídica':'', 'Página Web':'','Otras Webs':'','Marcas':'', 'Actividad':''}
        
        
#         for k in range(len(names)):
#             if k==4: continue
#             name = names[k].text
           
#             value = ''
#             if name in company_details_header:
#                 print("name=:",name,"K=:", k)
#                 value = driver.find_element(By.XPATH,f'//*[@id="row_2col_izq_big"]/div[1]/div[2]/table/tbody/tr[{k+1}]/td[2]').text
#                 company_detail.update({name:value})      
#                 # try:
#                 #     address = 
#                 # except:
#                 #     address = ""
#                 # company_detail_result = [company_name, address, ] 
#                 continue
#         print("Loop:",k)    
            
#         company_details.append(company_detail)     

#     csv_file = 'company_details.csv'
#     with open(csv_file, 'a', newline='', encoding='utf-8') as data_file1:
#         writer = csv.writer(data_file1)
#         writer.writerows(company_details)

driver.close()

