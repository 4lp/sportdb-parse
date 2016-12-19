import os, sys, getopt
import time

def main(argv):
	inputfile = ''
	outputfile = ''
	formattedContent = []
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print ('test.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('test.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"): 
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		else:
			print('error')
			sys.exit()
	with open(inputfile) as f:
		content = f.read()
		content = content.replace("[","")
		content = content.replace("]","")
		content = content.replace("\'","")
		content = content.split(",")
	for line in content:
		if (line != "" and line != " " and line != "  " and not line.endswith(")") and not line.startswith("(")):
			formattedContent.append(line)
	writeFile(parseFile(formattedContent), outputfile)

def parseFile(content):
	lines = ''
	count = 0
	date = ''
	team1 = ''
	team2 = ''
	score = ''
	matchday = 1
	formattedLines = []
	for line in content:
		#Is there a team this would conflict with?
		if ("Round " in line or "Final" in line or "Semi-finals" in line or "Week" in line):
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

if __name__ == "__main__":
	main(sys.argv[1:])