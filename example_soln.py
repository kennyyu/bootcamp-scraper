import bs4
import urllib

AMAZON_URL = "http://www.amazon.com/s/?keywords=ocaml"

def float_of_money(s):
    """
    Converts the money string to a float. For amounts in the format
        $30.00 - $65.00
    this will return the maximum bound as a float (65.00)
    """
    s = str(s)
    s = s.replace(",", "") # Remove commas in numbers
    return float(s[s.rfind("$") + 1:])

# TODO: write a function that returns True if the tag is a div,
# has an id, and has an id that starts with "result_"
def is_result_div(tag):
    if not tag.name == "div":
        return False
    return tag.has_key("id") and str(tag["id"]).startswith("result_")

if __name__ == "__main__":
    # get html webpage
    urlobject = urllib.urlopen(AMAZON_URL)

    # create a beautiful soup object to read data from the webpage
    soup = bs4.BeautifulSoup(urlobject.read())

    # print title of web page
    print soup.title
    print soup.title.text

    # find all divs with ids starting with "result_"
    result_divs = soup.find_all(is_result_div)
    print len(result_divs)

    # print out first one to see structure
    if len(result_divs) > 0:
        print result_divs[0]

    # loop over all results
    for result_div in result_divs:
        # holds general information about product
        title_div = result_div.find(class_="productTitle")

        # TODO: extract link from title_div
        link = title_div.a["href"]

        # TODO: extract title
        # lstrip() removes extra white spaces
        title = str(title_div.a.string).lstrip()

        # TODO: extract author if it exists
        author = ""
        if title_div.span is not None:
            # remove all the links and extra stuff to just get the text
            text = "".join(map(lambda z: str(z.string),
                               title_div.span.contents))

            # remove extra whitespace
            text_no_white = text.lstrip()

            # remove the "by" in "by John Doe"
            author = text_no_white[3:]

        # divs that hold new and used prices
        new_price_div = result_div.find(class_="newPrice")
        used_price_div = result_div.find(class_="usedNewPrice")

        # TODO: extract used and new prices
        # HINT: use float_of_money
        new_price = 0.
        if new_price_div is not None:
            new_price = float_of_money(new_price_div.span.string)

        used_price = 0.
        if used_price_div is not None and used_price_div.div.span is not None:
            used_price = float_of_money(used_price_div.div.span.string)

        # all the information we want!
        print (title, author, link, new_price, used_price)

