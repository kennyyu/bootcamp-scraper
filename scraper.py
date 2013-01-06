import argparse
import bs4
import csv
import urllib

# URL for searching for products on amazon
AMAZON_URL = "http://www.amazon.com/s/?keywords="

# Specify command line arguments
argparser = argparse.ArgumentParser("Web scraper for Amazon")
argparser.add_argument("-s", "--search", type=str, dest="search",
                       required=True, help="search to scrape")
argparser.add_argument("-o", "--outfile", type=str, dest="outfile",
                       default="data.csv", help="out file for csv data")

def remove_non_ascii(s):
    """ Remove non ascii characters (e.g. unicode). """
    return "".join(filter(lambda x: ord(x) < 128, s))

class Result:
    """ Encapsulates a result of a search query. """

    def __init__(self, link, title, author, new_price, old_price):
        self.link = link
        self.title = title
        self.author = author
        self.new_price = new_price
        self.old_price = old_price

    def __str__(self):
        return "link: %s\ntitle: %s\nauthor: %s\nnew:  %f\nold: %f" % \
            (self.link, self.title, self.author, self.new_price, self.old_price)

def is_result_div(tag):
    """ Returns true for divs with ids starting with 'result_'. """
    if not tag.name == "div":
        return False
    return tag.has_key("id") and str(tag["id"]).startswith("result_")

def get_items(html):
    # list to keep track of our extracted values
    results = []

    # results will be in divs with ids "result_1, result_2, ..."
    soup = bs4.BeautifulSoup(html)
    result_divs = soup.find_all(is_result_div)
    for result_div in result_divs:
        title_div = result_div.find(class_="productTitle")
        new_price_div = result_div.find(class_="newPrice")
        used_price_div = result_div.find(class_="usedNewPrice")

        # Extract the fields that we want
        link = title_div.a["href"]
        title = str(remove_non_ascii(title_div.a.string)).lstrip()

        # Concatenate all the text elements together into a string
        author = "".join(map(lambda z: str(remove_non_ascii(z.string)),
                             title_div.span.contents)).lstrip()[3:]

        # Remove $ sign and return amount as a float.
        new_price = 0.
        if new_price_div is not None:
            new_price = float(str(new_price_div.span.string)[1:])
        used_price = 0.
        if used_price_div is not None:
            used_price = float(str(used_price_div.div.span.string)[1:])

        # Create a result object to encapsulate the fields that we want
        result = Result(link, title, author, new_price, used_price)
        results.append(result)
    return results

def write_csv(filename, results):
    """ Write results in csv format to filename. """
    csvfile = open(filename, "wb")
    writer = csv.DictWriter(csvfile, 
                            ["title", "author", "link",
                             "new_price", "old_price"])
    writer.writeheader()
    for result in results:
        writer.writerow(result.__dict__) # get dict of the object's attributes
    csvfile.close()

def main(search, outfile):
    page = 1
    results = []

    # Keep scraping all the pages until we find a page with no results.
    while True:
        urlobject = urllib.urlopen(AMAZON_URL + search + "&page=" + str(page))
        new_results = get_items(urlobject.read())
        if len(new_results) == 0:
            break
        else:
            results += new_results
            page += 1
    write_csv(outfile, results)

if __name__ == "__main__":
    args = vars(argparser.parse_args())
    main(search=args["search"], outfile=args["outfile"])
