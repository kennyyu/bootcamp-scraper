import argparse
import bs4
import urllib
import sys

AMAZON_URL = "http://www.amazon.com/s/?field-keywords="

argparser = argparse.ArgumentParser("Web scraper using Beautiful Soup")
argparser.add_argument("-s", "--search", type=str, dest="search",
                       help="search to scrape")

def is_result_div(tag):
    if not tag.name == "div":
        return False
    return tag.has_key("id") and str(tag["id"]).startswith("result_")

def get_items(html):
    soup = bs4.BeautifulSoup(html)
    result_divs = soup.find_all(is_result_div)
    for result_div in result_divs:
        title = result_div.find(class_="productTitle")
        new_price = result_div.find(class_="newPrice")
        used_price = result_div.find(class_="usedNewPrice")
        print title.a["href"]
        print str(title.a.string).lstrip()
        print "".join(map(lambda z: str(z.string), title.span.contents)).lstrip()
        if new_price is not None:
            print "new:  " + str(new_price.span.string)
        if used_price is not None:
            print "used: " + str(used_price.div.span.string)
        print ""

if __name__ == "__main__":
    args = vars(argparser.parse_args())
    if args["search"] is None:
        print "must provide seach query, run with -h option for help"
        sys.exit(-1)
    url = AMAZON_URL + args["search"]
    urlobject = urllib.urlopen(url)
    get_items(urlobject.read())