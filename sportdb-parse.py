import os, sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
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
	writeFile(parseFile(inputfile), outputfile)

def parseFile(fname):
	lines = ''
	with open(fname) as f:
		content = f.readlines()
	f.close()
	count = 0
	date = ''
	team1 = ''
	team2 = ''
	score = ''
	formattedLines = []
	for line in content:
		if "Round " in line:
			formattedRoundLine = formatRoundLine(line.rstrip())
			formattedLines.append(formattedRoundLine)
		elif count % 4 == 0:
			date = line.rstrip()
			count += 1
		elif count % 4 == 1:
			team1 = line.rstrip()
			count += 1
		elif count % 4 == 2:
			team2 = line.rstrip()
			count += 1
		elif count % 4 == 3:
			score = line.rstrip()
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