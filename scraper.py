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
argparser.add_argument("-p", "--page", type=int, dest="page",
                       default=1, help="page number to start scraping")
argparser.add_argument("-a", "--append", dest="append", action="store_true",
                       default=False, help="append to output file")

def remove_non_ascii(s):
    """ Remove non ascii characters (e.g. unicode). """
    if s is None:
        return ""
    return "".join(filter(lambda x: ord(x) < 128, s))

def float_of_money(s):
    """
    Converts the money string to a float. For amounts in the format
        $30.00 - $65.00
    this will return the maximum bound as a float (65.00)
    """
    s = str(s)
    s = s.replace(",", "") # Remove commas in numbers
    return float(s[s.rfind("$") + 1:])

class Result:
    """ Encapsulates a result of a search query. """

    def __init__(self, link, title, author, new_price, used_price):
        self.link = link
        self.title = title
        self.author = author
        self.new_price = new_price
        self.used_price = used_price

    def __str__(self):
        return "link: %s\ntitle: %s\nauthor: %s\nnew:  %f\nused: %f" % \
            (self.link, self.title, self.author,
             self.new_price, self.used_price)

def is_result_div(tag):
    """ Returns true for divs with ids starting with 'result_'. """
    if not tag.name == "div":
        return False
    return tag.has_key("id") and str(tag["id"]).startswith("result_")

def get_results(html):
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
        author = ""
        if title_div.span is not None:
            author = "".join(map(lambda z: str(remove_non_ascii(z.string)),
                                 title_div.span.contents)).lstrip()[3:]

        # Remove $ sign and return amount as a float
        new_price = 0.
        if new_price_div is not None:
            new_price = float(float_of_money(new_price_div.span.string))
        used_price = 0.
        if used_price_div is not None and used_price_div.div.span is not None:
            used_price = float(float_of_money(used_price_div.div.span.string))

        # Create a result object to encapsulate the fields that we want
        result = Result(link, title, author, new_price, used_price)
        results.append(result)
    return results

def write_results(writer, results):
    """ Write results in csv format to filename. """
    for result in results:
        writer.writerow(result.__dict__) # get dict of the object's attributes

def main(search, outfile, page, append):
    # Create file to append csv results and write the header columns
    csvfile = open(outfile, "wb") if not append else open(outfile, "ab")
    writer = csv.DictWriter(csvfile,
                            ["title", "author", "link",
                             "new_price", "used_price"])
    if not append:
        writer.writeheader()

    # Keep scraping all the pages until we find a page with no results.
    total = 0
    while True:
        print "Scraping page %d..." % page
        urlobject = urllib.urlopen(AMAZON_URL + search + "&page=" + str(page))
        results = get_results(urlobject.read())
        nresults = len(results)
        if nresults == 0:
            print "Done!"
            break
        else:
            write_results(writer, results)
            csvfile.flush()
            total += nresults
            print "Scraped %d results from page %d, total results: %d" % \
                (nresults, page, total)
            page += 1

    # Close our file handle
    csvfile.close()

if __name__ == "__main__":
    args = vars(argparser.parse_args())
    main(**args)
