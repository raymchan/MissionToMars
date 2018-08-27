# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from datetime import datetime
import time


# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "chromedriver"}
    # return Browser("chrome", **executable_path)


def scrape():
    
    #--------------NASA MARS NEWS------------------------
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # time.sleep(5)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve page with the requests module
    # response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html,'lxml')
    print(soup)

    results = soup.find_all("div", class_='slide')
    # print(results)

    for result in results:

        title=result.find("div", class_='content_title')
    #     print(title)

        paragraph=result.find("div", class_="rollover_description_inner")
    #     print(paragraph)

        title_text = title.text
    #     print(title_text)

        para_text = paragraph.text
    #     print(para_text)


    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

    # * Make sure to find the image url to the full size `.jpg` image.

    # * Make sure to save a complete url string for this image.
    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

     #--------------JPL MARS SPACE IMAGES------------------------
    
    # Initialize browser
    # browser = init_browser()

    # Visit the page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # featured_image_url
    featured_image_url="https://www.jpl.nasa.gov"+soup.find("article")['style'].split("('", 1)[1].split("')")[0]
    # print(featured_image_url)




    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    
     #--------------NASA MARS WEATHER------------------------

    # Initialize browser
    # browser = init_browser()

    # Visit the url
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    # mars_weather
    mars_weather=soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # print(mars_weather)


    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    # * Use Pandas to convert the data to a HTML table string.
    
     #--------------NASA MARS FACTS------------------------
    # Initialize browser
    # browser = init_browser()

    # Visit the url
    url = "http://space-facts.com/mars/"
    # browser.visit(url)

    # Scrape page into soup
    # html = browser.html
    # soup = BeautifulSoup(html, "html.parser")

    # print(soup.find("table", class_="tablepress tablepress-id-mars"))
    # table=(pd.read_html(soup.find("table", class_="tablepress tablepress-id-mars").prettify(),skiprows=2))[0]

    table=pd.read_html(url)[0].rename(index=str, columns={"0": "Category", "1": "Fact"})
    html_table=table.to_html(na_rep = "",index=False)


    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.

    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Initialize browser
    # browser = init_browser()

    # Visit the url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # hemisphere_image_url_1

    results = soup.find_all("div", class_='description')
    print(results)

    mars_data = []
    mars_dict = {}

    for result in results:

    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

        image_url_loc="https://astrogeology.usgs.gov"+result.find("a", href=True)["href"]
    #     print(image_url_loc)

        # Initialize browser
        # browser = init_browser()

        # Visit the url
        browser.visit(image_url_loc)

        # Scrape page into soup
        html = browser.html
        soup1 = BeautifulSoup(html, "html.parser")

        image_url ="https://astrogeology.usgs.gov" + soup1.find("img", class_='wide-image')['src']
    #     print(image_url)

        title=result.find("h3").text
    #     print(title)

        mars_dict = {
            "title": title,
            "img_url" : image_url
        }

        mars_data.append(mars_dict)

    mars_scrape_results={
        "newstitle":title_text,
        "newsparagraph":para_text,
        "featuredimage":featured_image_url,
        "marsfacts":html_table,
        "marsweather":mars_weather,
        "marsdata":mars_data,
    }
    
    return mars_scrape_results

