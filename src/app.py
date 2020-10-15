from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.sql import select, insert
from bs4 import BeautifulSoup
import sqlalchemy
from cup import Cup
import os, time
import create_database as db
import telegramBot as tb

db.setUp()
conn = db.getDbConnection().connect()
db_cups = db.getUserTable()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

cups_saved = []
no_cups_found_counter = 0
s = select([db_cups])
result = conn.execute(s)
for row in result:
  cup_temp = Cup(row['gender'], row['date'], row['category'], row['name'], row['players'], row['link'])
  cups_saved.append(cup_temp)

while True:
  # Reload the page with webdriver and get cups into soup2 
  if no_cups_found_counter > 10:
    tb.send_message_no_cups_found()

  driver.get("https://www.beachvolleyball.nrw")
  try:
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".table-tournaments.table.table-hover")))
  except selenium.common.exceptions.TimeoutException as e:
    print("Was not able to retrieve Webpage, will try again in 60 Seonds!")
    no_cups_found_counter++
    time.sleep(60)
    break
  soup1 = BeautifulSoup(driver.page_source, 'lxml')
  soup2 = soup1.find_all("tr", class_=lambda value: value and value.startswith("series"))
  cups_found = []
  # Extract information of each cup
  try:
    for cup in soup2:
      no_cups_found_counter = 0
      g_gender = cup['class'][0]
      if g_gender[7] == 'm':
        a_gender = 'Mixed'
      elif g_gender[7] == 'h':
        a_gender = 'Herren'
      elif g_gender[7] == 'd':
        a_gender = 'Herren'
      else:
        a_gender = 'Senioren'
      date = cup.find('td', class_="date").get_text()
      category = cup.find('span', class_="category-shorthandle").get_text()
      name = cup.find('a').get_text()
      players = cup.find('td', class_="players").get_text()
      for l in cup.findAll('a'):
        link = 'https://www.beachvolleyball.nrw/' + l.get('href')
      cups_found.append(Cup(a_gender, date, category, name, players, link))
  except IndexError as e:
    print(e)
    print('Cup that caused the IndexError: ', cup)
    print('Propably someone misstyped when creating a cup!!')

  #Compare the found cups with the cups already found and saved in cups_saved
  cup_found = False
  for cup in cups_found:
    if cup not in cups_saved:
      cup_found = True
      print('FOUND NEW CUP!')
      #Add cup to the saved list
      cups_saved.append(cup)
      
      # insert() expects lmdb but is not neccessary, problem between sqlalchemy and pylint
      ins = db_cups.insert().values(id=cup.id, gender=cup.gender, date=cup.date, category=cup.category, name=cup.name, players=cup.players, link=cup.link)
      try:
        result = conn.execute(ins)
      except sqlalchemy.exc.IntegrityError as e:
          print()
          print(e)
          print(cup)
          print()
      tb.send_message(f'{cup.link} \nNeuer {cup.gender}-Cup in {cup.name} am {cup.date} \nAngemeldet sind : {cup.players} Teams \n')
  if cup_found == False:
    print('Was not able to find new cups!')
  time.sleep(60)

# end of program