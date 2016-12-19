#list of urls to scrape - populated as example
$urllist = "http://www.scoreboard.com/soccer/zambia/super-league-2015/results/", "http://www.scoreboard.com/soccer/zambia/super-league-2014/results/"

foreach ($url in $urllist) {
	python .\sportdb-scrape.py -i $url
}