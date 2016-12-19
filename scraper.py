from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
# import win_unicode_console
from contextlib import closing
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
import os
import time
import re

#only for print() testing
#win_unicode_console.enable()

driver = webdriver.Firefox(firefox_binary=FirefoxBinary(
        firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'
        ))

def writeFile(content, saveLoc):
	saveLoc = os.path.normpath(saveLoc)
	file = open(saveLoc,"w")
	file.write(str(content))
	file.close()

with closing(Firefox()) as driver:
	driver.get("http://www.scoreboard.com/soccer/england/championship-2014-2015/results/")
	button = driver.find_element_by_xpath("//*[@id='tournament-page-results-more']/tbody/tr/td/a")
	while(button):
		try:
			button.click()
			# wait for the page to load
			# WebDriverWait(driver, 10).until(
			# EC.invisibility_of_element_located((By.ID, "fs-overlay")
			# ))
			# WebDriverWait(driver, 10).until(
			# EC.element_to_be_clickable((By.XPATH, "//*[@id='tournament-page-results-more']/tbody/tr/td/a")
			# ))
			# WebDriverWait(driver, 100).until(
			# EC.presence_of_element_located((By.XPATH, "//*[@id='fs-overlay'][@style='display: none']")
			# ))
			# couldn't get WebDriverWait to work so using hacky time.sleep in the interim
			time.sleep(2)
		except ElementNotVisibleException:
			if (button.is_displayed() == False):
				page_source = driver.page_source
				bsObj = BeautifulSoup(page_source, "html.parser")
				results = bsObj.find_all('tr', class_=re.compile(r"^(event_round|stage-finished)$"))
				saveLoc = ".\\results.txt"
				writeFile(results, saveLoc)
				print("done!")
				exit()
			else:
				print(button.is_displayed())
		except TimeoutException:
			pass

driver.quit()