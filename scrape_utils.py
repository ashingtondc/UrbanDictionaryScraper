from bs4 import BeautifulSoup
import requests as req
import re
from wrapper_mongodb import Entry
import logging

"""
is_wotd(panel)
Determines if a definition on an urban dictionary page is the WOTD, which is
not actually related to the term being scraped.

Params:
panel: A Beautiful Soup object containing the specific definition panel to be
evaluated.

Returns: 
bool
"""
def is_wotd(panel):
    ribbon = panel.find(attrs={"class":"ribbon"}).text
    if re.match("\\w+ \\d{1,2} Word of the Day", ribbon):
        return True
    return False


"""
process_term(url)
Parses the page at the given URL for all definitions of the term covered by the
page. 

Params:
url: A string pointing to the webpage to be scraped.

Returns:
A list of dictionaries. Each dictionary covers a separate definition of the
term, providing the title, definition, and an example. 
"""
def process_term(url):
    try:
        resp = req.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        word_info = soup.find_all(attrs={"class":"def-panel"})
        definitions = []
        for panel in word_info:
            if not is_wotd(panel):
                entry = {}

                word_title = panel.find(attrs={"class":"def-header"}).text
                word_definition = panel.find(attrs={"class":"meaning"}).get_text()
                word_example = panel.find(attrs={"class":"example"}).get_text()

                vote_panel = panel.find(attrs={"class":"up"})
                votes = int(vote_panel.find(attrs={"class":"count"}).get_text())

                entry['title'] = word_title
                entry['definition'] = word_definition
                entry['example'] = word_example
                entry['votes'] = votes

                print(word_title, votes)

                definitions.append(entry)
        return definitions
    except:
        return []

def scrape_letter(i):
    url = "https://www.urbandictionary.com/browse.php?character=" + chr(i)
    logging.info("Scraping letter " + chr(i))

    try:
        has_next_page = True
        while has_next_page:
            logging.info("Scraping page " + url)
            try:
                resp = req.get(url)
                soup = BeautifulSoup(resp.text, 'html.parser')
                words = soup.find(attrs={"id": "columnist"}).find_all('a')
                # print(words2)
                for word in words:
                    name = word.text
                    print(name)
                    word_url = "https://www.urbandictionary.com" + word.get('href')
                    try:
                        if len(name.split()) <= 3:
                            entry = {
                                "title": name,
                                "definition": process_term("https://www.urbandictionary.com" + word.get('href')),
                                "url": word_url
                            }
                            # Done: Insert entry in database
                            new_entry = Entry(entry)
                            new_entry.save()
                    except:
                        logging.error("Error while processing " + name + " at " + word_url)
                # Check if there is next page
                next_page = soup.find(attrs={"rel": "next"})
                if next_page:
                    url = "https://www.urbandictionary.com" + next_page.get('href')
                else:
                    has_next_page = False
            except:
                logging.error("Error while scraping " + url)
    except:
        logging.error("Error while scraping letter " + chr(i))