quick n' dirty script to convert soccer scores to sportdb format. uses selenium and beautiful soup to scrape page and python to convert html.

you will need to mess with sportdb-scrape.py - selenium 2 requires Firefox<45 (ESR) and I had to hard-code the path.

run `python ./sportdb-scrape.py -i [url]` e.g.  `python ./sportdb-scrape.py -i http://www.scoreboard.com/soccer/zambia/super-league-2015/results/` to scrape n' convert. saves output as 
`./[url]_results.txt` stripped of the main domain name and formatted for os filenames e.g. `./zambia_super-league-2014_results__results.txt`.

see `sportdb-scrape.ps1` for an example of using Powershell to automate scraping for an array of urls.