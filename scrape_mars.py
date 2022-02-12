# Dependencies 

from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_date, news_title, news_p = mars_news(browser)

    data = {
        "news_date": dt.datetime.now(),
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_data(),
        "hemispheres": hemisphere(browser)
    }

    browser.quit()
    return data

def mars_news(browser):
    url = "https://redplanetscience.com"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"html.parser")

    try:
        article = soup.find("div", class_="list_text")
        news_date = (soup.find_all('div', class_="list_date"))[0].get_text()
        news_title = article.find("div", class_="content_title").text
        news_p = article.find("div", class_="article_teaser_body").text
    
    except AttributeError:
        return None, None

    return news_date, news_title, news_p

def featured_image(browser):
    image_url = "https://spaceimages-mars.com"
    browser.visit(image_url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        image = soup.find("img", class_="headerimage fade-in")["src"]
        featured_image_url = "https://spaceimages-mars.com" + image

    except AttributeError:
        return None

    img_url = "https://spaceimages-mars.comimage/featured/mars2.jpg"

    return img_url

def mars_data():
    try:
        mars_facts = pd.DataFrame(pd.read_html("https://galaxyfacts-mars.com")[0])

    except BaseException:
        return None

    mars_facts.columns=["Properties", "Mars", "Earth"]
    mars_facts.set_index("Propeties", inplace=True)

    return mars_facts.to_html(classes="table table-striped")

def hemisphere(broswer):
    Mars_Hems_url = "https://marshemispheres.com"
    browser.visit(Mars_Hems_url)

    hemisphere_image_urls = []

    for i in range(4):
    
    #create empty dictionary
    hemispheres = {}
    
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.find_link_by_text('Sample').first
    Mars_Hems_url = element['href']
    title = browser.find_by_css("h2.title").text
    hemispheres["Mars_Hems_url"] = Mars_Hems_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()

return hemisphere_image_urls

if __name__ == "__main__":

    print(scrape_all())

