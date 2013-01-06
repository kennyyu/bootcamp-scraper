Web Scraper for Amazon
======================

By Kenny Yu

## Description

This is an example of a web scraper that queries Amazon with the given search phrase and outputs a csv file containing the resulting data.

## Dependencies

* [Beautiful Soup 4.1.3](http://www.crummy.com/software/BeautifulSoup/)
* [Python 2.7](http://www.python.org/download/releases/2.7/)

## How to Run the Scraper

To see options for the scraper, run:

    python scraper.py -h

The default out file is `data.csv`. To specify a different file, use the `-o`/`--outfile` flag. For example, to query amazon for `ocaml` and to save the results in `ocaml.csv`, run:

    python scraper.py ocaml --outfile=ocaml.csv

This should create the file `ocaml.csv` in the current directory with column headers `title,author,link,new_price,used_price`. To start scraping at a different page, use the `-p`/`--page` flag:

    python scraper.py "introduction to algorithms" --outfile=alg.csv --page=3

To append to an already existing csv file, use the `-a`/`--append` flag:

    python scraper.py haskell --outfile=ocaml.csv --append

The results of this search will be appended to the end of `ocaml.csv`.