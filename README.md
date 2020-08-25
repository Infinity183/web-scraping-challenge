# web-scraping-challenge

For this project, I scraped data from a variety of webistes about mars, including articles, images, and fact tables, and used a Flask app to store this information into MongoDB by calling a scraper app. From there, I used the stored data from the Mongo database to design a website that put everything together on a single page. The page also includes a button to scrape the data all over again, in case the retrieved articles and images change with time.

File Guide:
  * mission_to_mars.ipynb - This is the Jupyter notebook I created to execute the web scraping processes. Each step is explained.
  * mars_scraper.py - This is the Python code used to scrape data from the web to be stored for reference in the Flask app.
  * app.py - This is the Flask app, which establishes a Mongo connection and uses mars_scraper to store the Mars info into a database.
  * mars_facts_table.html - This is just the html version of the table I scraped from the web.
  * Picture_of_Website.png - A screenshot of the website once it's visited.
  * chromedriver.exe - Needed to run the Flask app.
  * Templates - This folder contains the index html file.
