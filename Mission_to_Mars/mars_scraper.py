from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def start_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scraper():
    browser = start_browser()
    mars_data = {}

    # NASA Articles
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soupy = bs(html, 'html.parser')
    stories = soupy.find(class_='item_list')
    content_title = stories.find(class_='content_title')
    link = content_title.find('a')['href']
    mars_data['nasa_article_title'] = content_title.find('a').text

    basic_url = 'https://mars.nasa.gov'
    article_url = basic_url + link
    browser.visit(article_url)
    html_another = browser.html
    soupy_another = bs(html_another, 'html.parser')
    story_another = soupy_another.find(class_='wysiwyg_content')
    paragraphs = story_another.find_all('p')
    mars_data['first_paragraph'] = paragraphs[1].text

    # JPL Image
    jpl_base = 'https://www.jpl.nasa.gov'
    mars_image_extension = '/spaceimages/?search=&category=Mars#submit'
    mars_images = jpl_base + mars_image_extension
    browser.visit(mars_images)
    html_jpl = browser.html
    soupy_jpl = bs(html_jpl, 'html.parser')
    bg_image = soupy_jpl.find('article', class_='carousel_item')
    page_images = soupy_jpl.find_all('img')
    first_image = page_images[5]['src']
    mars_data['first_jpl_image'] = jpl_base + first_image
    featured_image_url = bg_image['style'].split("('", 1)[1].split("')")[0]
    mars_data['featured_jpl_image'] = jpl_base + featured_image_url

    # Mars Facts Table
    mars_facts_url = 'https://space-facts.com/mars/'
    table_facts = pd.read_html(mars_facts_url)
    facts_table = table_facts[0]
    facts_table.columns = ['', 'answers']
    facts_table.set_index('', inplace=True)
    facts_table.columns = ['']
    html_version = facts_table.to_html()
    html_version_cleaned = html_version.replace('\n', '')
    mars_data['mars_facts_table'] = html_version_cleaned
    facts_table.to_html('mars_facts_table.html')

    # Four Hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soupy_hemispheres = bs(html_hemispheres, 'html.parser')
    results = soupy_hemispheres.find(class_='collapsible results')
    hemispheres_list = results.find_all(class_='item')
    image_links = []
    for hemisphere in hemispheres_list:
        link_location = hemisphere.find('a')
        hemisphere_extension = link_location['href']
        hemisphere_page = 'https://astrogeology.usgs.gov' + hemisphere_extension
        browser.visit(hemisphere_page)
        html_hemi = browser.html
        soupy_hemi = bs(html_hemi, 'html.parser')
        list_item = soupy_hemi.find('li')
        destination = list_item.find('a')
        image_links.append(destination['href'])
    hemisphere_keys = ['cerebus', 'sciaparelli', 'syrtis_major', 'valles_marineris']
    hemisphere_image_dictionary = {}
    for x in range(0, len(image_links)):   
        hemisphere_image_dictionary.update( {hemisphere_keys[x]: image_links[x]})
    mars_data['four_hemispheres'] = hemisphere_image_dictionary
    browser.quit()

    return mars_data