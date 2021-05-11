from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.sql import select, insert
from bs4 import BeautifulSoup
import sqlalchemy
from cup import Cup
import os
import time
import create_database as db
import telegramBot as tb

db.setUp()
conn = db.getDbConnection().connect()
db_cups = db.getUserTable()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path='/usr/local/bin/chromedriver', options=options)
driver4x4 = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
cups_saved = []
no_cups_found_counter = 0
s = select([db_cups])
result = conn.execute(s)
for row in result:
    cup_temp = Cup(row['gender'], row['date'], row['category'],
                   row['name'], row['players'], row['link'], row['inform'])
    cups_saved.append(cup_temp)

while True:
    # Reload the page with webdriver and get cups into soup2
    if no_cups_found_counter > 10:
        tb.send_message_no_cups_found()

    driver.get(
        "https://www.beachvolleyball.nrw/?series=&tournamentsPage=1&tournamentsLimit=800")
    
    driver4x4.get("https://www.beachvolleyball.nrw/?series=&tournamentsLimit=800&tournamentsPage=1&tt=4x4")
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))
            
        WebDriverWait(driver4x4, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))
    except:
        print("Was not able to retrieve Webpage, will try again in 5 Minutes!")
        no_cups_found_counter += 1
        time.sleep(300)
    soup1 = BeautifulSoup(driver.page_source, 'lxml')
    soup4x4 = BeautifulSoup(driver4x4.page_source, 'lxml').find_all(
        "tr", class_=lambda value: value and value.startswith("series"))
    soup2 = soup1.find_all(
        "tr", class_=lambda value: value and value.startswith("series"))
    soup2 += soup4x4
    cups_found = []
    # Extract information of each cup
    try:
        for cup in soup2:
            no_cups_found_counter = 0
            inform = 1
            s = cup['class'][0]
            #print('\nthis is s:    ', s)
            start = 'series-'
            g_gender = s.replace(start, '')
            if g_gender == 'm':
                a_gender = 'Mixed'
            elif g_gender == 'h':
                a_gender = 'Herren'
            elif g_gender == 'd':
                a_gender = 'Damen'
            elif g_gender == 'u':
                a_gender = 'Jugend'
                inform = 0
            elif g_gender == 'uw':
                a_gender = 'Jugend-Damen'
                inform = 0
            elif g_gender == 'um':
                a_gender = 'Jugend-Herren'
                inform = 0
            elif g_gender == 'uem':
                a_gender = 'Senioren-Herren'
                inform = 0
            elif g_gender == 'uew':
                a_gender = 'Senioren-Damen'
                inform = 0
            elif g_gender == '4x4_d':
                a_gender = '4x4-Damen'
            elif g_gender == '4x4_h':
                a_gender = '4x4-Herren'
            elif g_gender == '4x4_m':
                a_gender = '4x4-Mixed'
            elif g_gender == '4x4_um':
                inform = 0
                a_gender = '4x4-Jugend-Herren'
            elif g_gender == '4x4_uw':
                a_gender = '4x4-Jugend-Damen'
                inform = 0
            elif g_gender == '4x4_u':
                a_gender = '4x4-Jugend-Mixed'
                inform = 0
            else:
                a_gender = 'Sonder'
            date = cup.find('td', class_="date").get_text()
            category = cup.find(
                'span', class_="category-shorthandle").get_text()
            name = cup.find('a').get_text()
            players = cup.find('td', class_="players").get_text()
            for l in cup.findAll('a'):
                link = 'https://www.beachvolleyball.nrw' + l.get('href')
            cups_found.append(
                Cup(a_gender, date, category, name, players, link, inform))
    except IndexError as e:
        print(e)
        print('Cup that caused the IndexError: \n', cup.prettify())
        print('Propably someone misstyped when creating a cup!!')

    # Compare the found cups with the cups already found and saved in cups_saved
    cup_found = False
    for cup in cups_found:
        if cup not in cups_saved:
            cup_found = True
            print('FOUND NEW CUP!')
            # Add cup to the saved list
            cups_saved.append(cup)

            # insert() expects lmdb but is not neccessary, problem between sqlalchemy and pylint
            print()
            ins = db_cups.insert().values(id=cup.id, gender=cup.gender, date=cup.date,
                                          category=cup.category, name=cup.name, players=cup.players, link=cup.link, inform=cup.inform)
            try:
                result = conn.execute(ins)
            except sqlalchemy.exc.IntegrityError as e:
                print()
                print(e)
                print(cup)
                print()
            if cup.inform == 1:
                tb.send_message(
                    f'{cup.link} \nNeuer {cup.category} {cup.gender}-Cup in {cup.name} am {cup.date} \nAngemeldet sind : {cup.players} Teams \n')
            else:
                print('Did not want to inform about new Cup!')
    if cup_found == False:
        print('Was not able to find new cups! Will try again in 30 Minutes')
    time.sleep(1800)
