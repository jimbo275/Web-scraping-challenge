# Define a function called `scrape` that will execute all of your scraping code from the `mission_to_mars.ipynb` notebook and return one Python dictionary containing all of the scraped data. 

# It will be a good idea to create multiple smaller functions that are called by the `scrape()` function. 
# Remember, each function should have one 'job' (eg. you might have a `mars_news()` function that scrapes the NASA mars news site and returns the content as a list/tuple/dictionary/json)
# HINT: the headers in the notebook can serve as a useful guide to where one 'job' ends and another begins. 

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urldefrag
import time

# Get NASA news
# Import Splinter, BeautifulSoup, and Pandas

def scrape():
 # Path to chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

# Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
# Optional delay for loading the page
    time.sleep(10)
# Convert the browser html to a soup object and then quit the browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# .find() the content title and save it as `news_title`
    news_title = soup.find_all('div', class_='content_title')[1].find(target="_self").text

# .find() the paragraph text
    para_texts = soup.find_all('div', class_="article_teaser_body")[1].text
# quit the browser so it doesn't stay open
    browser.quit()


# Get JPL space image
# This library enables us to join relative urls to a root url to create an absolute url

    # Visit JPL space images Mars URL 
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    time.sleep(10)
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


# Import Mars facts
# Create a dataframe from the space-facts.com mars page

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    mars_df = tables[1].set_index("Mars - Earth Comparison")

# clean the dataframe and export to HTML
    mars_df.replace('\n', '')
    mars_html = mars_df.to_html('mars.html',index=False)


# Get hemisphere data
# visit the USGS astrogeology page for hemisphere data from Mars
    # visit the USGS astrogeology page for hemisphere data from Mars
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

# Build the list of enhanced urls
    hemi_image_urls = []
    enhanced_url_list = []
    hemi_all = soup.find_all('div', class_='item')

    for hemi in hemi_all:
        title = hemi.find('h3').text
        enhanced_url = hemi.a['href']
        enhanced_url = f'https://astrogeology.usgs.gov{enhanced_url}'
        enhanced_url_list.append(enhanced_url)
    


    # Build a list of dictionaries with the title and images    
    for enh_url in enhanced_url_list:   
        browser.visit(enh_url)
        time.sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        org_hemi_url = soup.find('div', class_='downloads').a['href']
        hemi_image_urls.append({"title": title, "img_url": org_hemi_url})
    
    scrape_dict = {
        "title": news_title,
        "para": para_texts,
        "featured_pic": featured_image_url,
        "html_tables": mars_html,
        "images": hemi_image_urls
    }


    browser.quit()
    return scrape_dict

