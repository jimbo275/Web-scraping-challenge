# Define a function called `scrape` that will execute all of your scraping code from the `mission_to_mars.ipynb` notebook and return one Python dictionary containing all of the scraped data. 

# It will be a good idea to create multiple smaller functions that are called by the `scrape()` function. 
# Remember, each function should have one 'job' (eg. you might have a `mars_news()` function that scrapes the NASA mars news site and returns the content as a list/tuple/dictionary/json)
# HINT: the headers in the notebook can serve as a useful guide to where one 'job' ends and another begins. 

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urldefrag

def image():
    # Get NASA news
# Import Splinter, BeautifulSoup, and Pandas

# def news():
#     news = {}
# # Path to chromedriver
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)

# # Visit the mars nasa news site
#     url = 'https://mars.nasa.gov/news/'
#     browser.visit(url)
# # Optional delay for loading the page

# # Convert the browser html to a soup object and then quit the browser
#     html = browser.html

#     soup = BeautifulSoup(html, 'html.parser')

# # .find() the content title and save it as `news_title`
#     news_title = soup.find_all('div', class_='content_title')[1].find(target="_self").text

# # .find() the paragraph text
#     para_texts = soup.find_all('div', class_="article_teaser_body")[1].text

#     browser.quit()

#     news["title"] = news_title
#     news["paragraph"] = para_texts

# return news
# Get JPL space image
# This library enables us to join relative urls to a root url to create an absolute url


    # Visit JPL space images Mars URL 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find the more info button and click that. 
    try:
        browser.links.find_by_partial_text('FULL IMAGE').click()
        html_image = browser.html
    except:
        print("Scraping Complete")
    finally:
        browser.quit()

    # Parse the resulting html with soup
    soup_image = BeautifulSoup(html_image, 'html.parser')

    # find the relative image url
    rel_url = soup_image.find_all('img', class_='fancybox-image')[0].attrs['src']

    # Use the base url to create an absolute url. Use urldefrag and urljoin to create a url and remove any extra folders in the filepath. Then select the first element in the resulting list    
    featured_image_url = urldefrag(urljoin(url, rel_url))[0]

    return {"url": featured_image_url}
# # Import Mars facts
# # Create a dataframe from the space-facts.com mars page
#     url = 'https://space-facts.com/mars/'
#     tables = pd.read_html(url)

#     mars_df = tables[1].set_index("Mars - Earth Comparison")

# # clean the dataframe and export to HTML
#     mars_df.replace('\n', '')
#     mars_html = mars_df.to_html('mars.html')

# # Get hemisphere data
# # visit the USGS astrogeology page for hemisphere data from Mars
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)
#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(url)

# # First, get a list of all of the hemispheres
#     hemi_list = []
#     html = browser.html
#     soup = BeautifulSoup(html, 'lxml')
#     hemis = soup.find_all('h3')
#     for hemi in hemis:
#         hemi_list.append(hemi.text)

#     browser.quit()
# # Next, loop through those links, click the link, find the sample anchor, return the href
# # Create a unique list of relative links using the set function. Do this because the same relative link is listed twice on the page. 
#     link_list = set()
#     hemi_names = soup.find_all('a', class_ ="itemLink product-item")
#     for val in enumerate(hemi_names):
#         link_list.add(val['href'])

# #convert the resulting set into a list and then sort them to get the links in order
#     sorted_link_list = list(sorted(link_list))

#     def make_url(stub: str) -> str:
#         _,_,_, planet, probe, location = stub.split('/')
#         return f'https://astropedia.astrogeology.usgs.gov/download/{planet}/{probe}/{location}.tif/full.jpeg'


# # Use a dictionary comprehrension to build the dictionary for the titles and their corresponding urls
#     title_dict = [{'img_url': make_url(href), 'title': title} for title, href in zip(hemi_list, sorted_link_list)]
    
#     listing = {}
#     listing["headline"] = news_title
#     listing["paragraph"] = para_texts
#     listing["featured_image"] = featured_image_url
#     listing["stats"] = mars_html
#     listing["hemi_list"] = hemi_list
#     listing["titles"] = title_dict

#     return listing