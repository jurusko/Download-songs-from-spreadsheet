#! python3
# konkurs2023.py - Open tabs with songs to download (year 2023).

import webbrowser, os, sys, bs4, time, shutil, selenium, cssselect, fnmatch, requests
import pyinputplus as pyip
import pandas as pd
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

def cookieAccept(): # Fuction of cookies' accept.
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, u"greenButtonCSS")))
        button = driver.find_element(By.CLASS_NAME, u"greenButtonCSS")
        ActionChains(driver).move_to_element(button).click(button).perform()
    finally:
        True

def login():
    print('Logging into account...')
    search_login = driver.find_element(By.XPATH, ('//*[@id="topBarLogin"]')).send_keys("jurasek") # Find login bar. Fill.
    search_password = driver.find_element(By.XPATH, ('//*[@id="topBarPassword"]')).send_keys("********", Keys.ENTER) # Find password bar. Fill.
    print('Logg in completed.')
    time.sleep(delay)

def minor_bars():
    proba = 0
    urlToOpen = "http://chomikuj.pl/action/SearchFiles"  # Go to website to search for those songs.
    while proba < 3:
        print('Looking for minor search bars.')
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SizeFrom"]')))
        except:
            proba += 1
            if proba == 3:
                os.system("taskkill /im chrome.exe /f")
        else:
            proba = 3
            clearsearch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SizeFrom"]')))  # Find search bar for min. size of song.
            clearsearch.click()
            clearsearch.clear()  # Purge the search bar.
            search_input_box2 = driver.find_element(By.XPATH, ('//*[@id="SizeFrom"]')).send_keys("1")  # Find search bar for min. size of song.
            clearsearch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "SizeTo"]')))  # Find search bar for max. size of song.
            clearsearch.click()
            clearsearch.clear()  # Purge the search bar.
            search_input_box3 = driver.find_element(By.XPATH, ('// *[ @ id = "SizeTo"]')).send_keys("9")  # Find search bar for max. size of song.
            clearsearch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Extension"]')))  # Find search bar for format of song.
            clearsearch.click()
            clearsearch.clear()  # Purge the search bar.
            search_input_box4 = driver.find_element(By.XPATH, ('//*[@id="Extension"]')).send_keys("mp3") # Find search bar for format of song.

def search_for_songs(lista):
    for i in range (len(lista)):
        time.sleep(delay)
        print(len(lista)-i, 'songs left to be downloaded.')
        print('Searching for song %s.' % lista[i])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FileName"]')))
        search_input_box1 = driver.find_element(By.XPATH, ('//*[@id="FileName"]')).send_keys(lista[i], Keys.ENTER) # Find search bar for name of song. Search.
        print('Results\' page is displayed.')

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="listView"]/div[3]/div[3]/h3/a/span')))
            search_result = driver.find_element(By.XPATH, ('//*[@id="listView"]/div[3]/div[3]/h3/a/span'))  # Find first result.
            search_result.click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "searchDownloadForm"] / button')))
            search_result_box = driver.find_element(By.XPATH, ('// *[ @ id = "searchDownloadForm"] / button'))  # Download button.
            search_result_box.click() # Start download.
            print('Start downloading song %s.' % lista[i])
        except:
            failed.append(lista[i])
            minor_bars()
        clearsearch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FileName"]'))) # Find search bar for name of song.
        clearsearch.click()
        clearsearch.clear() # Purge the search bar.

os.getcwd()
os.chdir(r'F:\!_Konkurs\Konkurs 2023') # Set working folder.
os.makedirs('mp3', exist_ok=True) # store mp3 in ./mp3 folder.

sheet = pd.read_excel('2023.xlsx', sheet_name='Utwory') # Open excel file and get list of songs.
df = pd.DataFrame(sheet)
wykonawcy = df.Wykonawca.values.tolist() # Column 'A'.
utwor = df.Utwór.values.tolist() # Column 'B'.
wyk_i_utw = []
failed = []
delay = 1 # Seconds.

for i in range(len(wykonawcy)):
    for j in range (len(utwor)):
        if i == j:
            wyk_i_utw.append(wykonawcy[i] + " " + utwor[j]) # Column 'A' plus column 'B' values(strings).

driver = webdriver.Chrome() # Choose browser.
urlToOpen = "http://chomikuj.pl/action/SearchFiles" # Go to website to search for those songs.
print('Opening', urlToOpen)
driver.get(urlToOpen)
print('Loading...') # Display text while loading page.

cookieAccept()
login()
minor_bars()
search_for_songs(wyk_i_utw)

dir_path = str(Path.home() / "Downloads") # Default browser download folder path.
count = len(fnmatch.filter(os.listdir(dir_path), '*.*')) # Count files in default browser download folder.
print('Files downloaded to: ', dir_path) # Display default browser download folder path.
print('Files downloaded: ', count) # Display number of files downloaded.
print('That means ',len(wyk_i_utw)-count, ' left. And those are:') # Display number of files not downloaded.
print(failed)