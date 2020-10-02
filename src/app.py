from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from cup import Cup
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

#driver = webdriver.Chrome(executable_path="c:/Users/frasb/AppData/Local/Programs/chromedriver/chromedriver.exe", options=options)
driver.get("https://www.beachvolleyball.nrw")

WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".table-tournaments.table.table-hover")))

soup1 = BeautifulSoup(driver.page_source, 'lxml')
soup2 = soup1.find_all("tr", class_=lambda value: value and value.startswith("series"))

cups = []

try:
  for cup in soup2:
    g_gender = cup['class'][0]
    if g_gender[7] == 'm':
      a_gender = 'Mixed'
    elif g_gender[7] == 'h':
      a_gender = 'Herren'
    elif g_gender[7] == 'd':
      a_gender = 'Herren'
    else:
      a_gender = 'Senioren'
except IndexError as e:
  print(e)
  print('Cup that caused the IndexError: ', cup)
  print('Propably someone misstyped when creating a cup!!')
  date = cup.find('td', class_="date").get_text()
  category = cup.find('span', class_="category-shorthandle").get_text()
  name = cup.find('a').get_text()
  players = cup.find('td', class_="players").get_text()
  for l in cup.findAll('a'):
    link = 'https://www.beachvolleyball.nrw/' + l.get('href')
  cups.append(Cup(a_gender, date, category, name, players, link))

for cup in cups:
  print(cup)

