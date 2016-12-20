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
from html.parser import HTMLParser
import sys
import unicodedata
import getopt

# only for print() testing
# win_unicode_console.enable()

driver = webdriver.Firefox(firefox_binary=FirefoxBinary(
        firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'
        ))

class rowParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []

	def handle_data(self, data):
		data = unicodedata.normalize("NFKD", data)
		#remove junk characters
		data = bytes(data, 'utf8').translate(None, b',\'')
		data = data.decode()
		self.data.append(data)

#convert.py

def convertFile(content):
	content = str(content)
	content = content.replace("[","")
	content = content.replace("]","")
	content = content.replace("\'","")
	content = content.split(",")
	print(content)
	lines = ''
	count = 0
	date = ''
	team1 = ''
	team2 = ''
	score = ''
	matchday = 1
	formattedLines = []
	for line in content:
		if (line != "" and line != " " and line != "  " and not line.endswith(")") and not line.startswith("(")):
			#Is there a team this would conflict with?
			if ("Round " in line or "Final" in line or "Semi-finals" in line or "Week" in line or "Quarter-finals" in line):
				formattedLines.append("\n%s\n" % line)
				matchday += 1
			elif count % 4 == 0:
				rawDate = line.strip().replace(",", "")
				date = time.strptime(rawDate, "%b %d %I:%M %p")
				date = time.strftime("%b %d", date)
				date = date.replace(" ", "/")
				count += 1
			elif count % 4 == 1:
				team1 = line.strip()
				count += 1
			elif count % 4 == 2:
				team2 = line.strip()
				count += 1
			elif count % 4 == 3:
				score = line.strip().replace(" : ", "-")
				formattedLine = formatLine(date, team1, team2, score)
				formattedLines.append(formattedLine)
				count += 1
	return formattedLines

def formatRoundLine(roundline):
	line = '%s' % roundline
	return line

def formatLine(date, team1, team2, score):
	line = '%s %s %s %s' % (date, team1, score, team2)
	return line

def writeFile(content, saveLoc):
	saveLoc = os.path.normpath(saveLoc)
	file = open(saveLoc,"w")
	for row in content:
		file.write(row + "\n")
	file.close()

def main(argv):
	inputfile = ''
	results = ''
	formattedContent = []
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print ('test.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('sportdb-scrape.py -i <url>')
			sys.exit()
		elif opt in ("-i", "--ifile"): 
			inputfile = arg
		else:
			print('error')
			sys.exit()

	#scrape
	with closing(Firefox()) as driver:
		driver.get(inputfile)
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
				time.sleep(5)
			except ElementNotVisibleException:
				page_source = driver.page_source
				bsObj = BeautifulSoup(page_source, "html.parser")
				results = bsObj.find_all('tr', class_=re.compile(r"^(event_round|stage-finished)$"))
				#parse.py
				parser = rowParser()
				parser.feed(str(results))
				data = parser.data
				#convert.py
				final = convertFile(data)
				#sanitize url for filename
				inputfile = inputfile.lstrip("http://www.scoreboard.com/")
				inputfile = inputfile.replace("/","_")
				saveLoc = ".\\%s_results.txt" % inputfile
				writeFile(final, saveLoc)
				driver.quit()
			except TimeoutException:
				pass

if __name__ == "__main__":
	main(sys.argv[1:])