from html.parser import HTMLParser
import os
import unicodedata

saveLoc = ".\\parseresults.txt"

def writeFile(content, saveLoc):
	saveLoc = os.path.normpath(saveLoc)
	file = open(saveLoc,"w")
	file.write(str(content))
	file.close()

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

parser = rowParser()
with open(os.path.normpath('./results.txt')) as f:
	content = f.read()
	f.close()
parser.feed(content)
writeFile(parser.data, saveLoc)