quick n' dirty script to convert soccer scores to sportdb format. uses selenium and beautiful soup to scrape page and python to convert html.

you will need to mess with scraper.py - selenium 2 requires Firefox<45 (ESR) and I had to hard-code the path.


works except for matchday/week/round designations - just change the url in scraper.py (`http://www.scoreboard.com/soccer/COUNTRY/LEAGUE/results/` e.g. `http://www.scoreboard.com/soccer/england/premier-league/results/`)

use scraper.py to get results page html (as `.\results.txt`)
use parse.py to parse html (as `.\parseresults.txt`)
user convert.py to convert to sportdb format (as `.\finalresults.txt`)