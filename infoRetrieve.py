"""
This this the script to extract data from all the databases(MySQL, MongoDB) using API
"""

# ------------------------------------Import packages we need and get linked with MySQL and MongoDB------------------------------------ #
# The API to connect Python with MySQL and MongoDB
# Make sure the MySQL is connected then in the Python we call it in the script
import pymysql
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re, requests, time
import pandas as pd
from datetime import datetime
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas.tools.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA

# Connect with MySQL
db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     passwd = '0325@tgiF',
                     db = 'redone512')

# Create an object 'cursor'
cursor = db.cursor()

# Connect with MongoDB
client = MongoClient('localhost', 27017)
# Set the db object to point to the business database
db = client.newsdata


# ------------------------------------Function to get the title or date or anything I want later from the website------------------------------------ #
def getTitle(n):
    title = 'NA'
    titleChunk = n.find('span', {'class': 'name'})
    if titleChunk:
        title = titleChunk.text
    return title

# Function to get the date og the news
def getDate(n):
    date = 'NA'
    dateChunk = n.find('span', {'class': 'date'})
    if dateChunk:
        date = dateChunk.text
    return date

# Scrape website with 'beautifulsoup'
def scraper(url):
    
    pageNum = 4 # Number of page to collect
    
    #fw = open('title.txt', 'w', encoding='utf-8')
    
    titleList = []
    dateList = []
    
    for p in range(1, pageNum + 1):
        print('page', p)
        html = None
        
        if p == 1:
            pageLink = url
        else:
            pageLink = url + '&start=' + str(10*(p-1)) + '&num=10' # Make the url link
        
        for i in range(5): # Try 5 times
            try:
                # Use the brower to access the url
                response = requests.get(pageLink, headers = { 'User-Agent': 
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
                html = response.content # Get the html
                break # When got the file, break the loop
            except Exception as e: # browser.open() threw an exception, the attempt to get the response failed
                print('failed attempt', i)
                time.sleep(2) # Wait 2 secs
                
        if not html:
            continue # Couldn't get the page, ignore
            
        soup = BeautifulSoup(html.decode('ascii', 'ignore'), 'lxml') # Parse the html 'html.parser'
        newsboard = soup.findAll('div', {'class': re.compile('g-section news sfe-break-bottom-16')})
        
        for n in newsboard:
            title = getTitle(n)
            date = getDate(n)
            titleList.append(title)
            dateList.append(date)
            time.sleep(2)
     
    return titleList, dateList

# Facebook 11.1
url = 'https://finance.google.com/finance/company_news?q=NASDAQ%3AFB&ei=rU4DWrjzC4GsmAG2p4TQCw'
# JP Morgan
url = 'https://finance.google.com/finance/company_news?q=NYSE%3AJPM&ei=mAf6WenLE46aeq-EkpAC'
# Apple
url = 'https://finance.google.com/finance/company_news?q=NASDAQ%3AAAPL&ei=pwj6WZm5FIarmAHvq5G4Aw'
# Amazon
url = 'https://finance.google.com/finance/company_news?q=NASDAQ%3AAMZN&ei=GAn6WYnlFZK2e5LttLgP'
# Tesla
url = 'https://finance.google.com/finance/company_news?q=NASDAQ:TSLA&ei=ZTn6WcnANtaie_D2obAH'

# A possible way to use this web crawler
mongoTitle = []
mongoDate = []
mongoTitle, mongoDate = scraper(url)


# ------------------------------------Create and Insert new information in MongoDB------------------------------------ #
ticker = ['AAPL', 'AMZN', 'FB', 'JPM', 'TSLA']
content = mongoTitle
date = mongoDate

# NoSQL command to create new records
for i in range(0, len(content)):
    result = db.FB.insert_one(
        {
                "Ticker": ticker[2],
                "Posted Date": mongoDate[i],
                "Content": mongoTitle[i].strip()
                }
        )

for i in range(0, len(content)):
    result = db.AAPL.insert_one(
        {
                "Ticker": ticker[0],
                "Posted Date": mongoDate[i],
                "Content": mongoTitle[i].strip()
                }
        )

for i in range(0, len(content)):
    result = db.AMZN.insert_one(
        {
                "Ticker": ticker[1],
                "Posted Date": mongoDate[i],
                "Content": mongoTitle[i].strip()
                }
        )

for i in range(0, len(content)):
    result = db.JPM.insert_one(
        {
                "Ticker": ticker[3],
                "Posted Date": mongoDate[i],
                "Content": mongoTitle[i].strip()
                }
        )

for i in range(0, len(content)):
    result = db.TSLA.insert_one(
        {
                "Ticker": ticker[4],
                "Posted Date": mongoDate[i],
                "Content": mongoTitle[i].strip()
                }
        )


# ------------------------------------Extract Data from MySQL and MongoDB------------------------------------ #
# Create a function to match and return data that saved in the MySQL and MongoDB
def searchData(ticker, date):
    #------------------------------------------------------
    # As this function is separated into two steps:
    # 1) Provide all the available information to the user
    # 2) Match and return the value that is required by the
    #    user. Set exceptions when a certain data is not in
    #    the database (MySQL, MongoDB).
    #------------------------------------------------------
    
    # SQL command
    tickerMySQL = 'SHOW TABLES'
    dateMySQL = 'SELECT date FROM %s' % (ticker)
    
    #------------------------------------------------------
    # From MySQL to Python script 
    # Get a list of tickers as they are the names of tables stored in MySQL
    cursor.execute(tickerMySQL)
    fetchTable = cursor.fetchall()
    table = []
    for i in range(len(fetchTable)):
        table.append(fetchTable[i][0])
    
    # Firsstly check whether we have the ticker stored
    if ticker not in table:
        print('Missing Ticker.')
    else:
        
        # SQL command
        priceMySQL = 'SELECT close FROM %s WHERE date = \'%s\'' % (ticker, date)
        infoMySQL = 'SELECT * FROM company_information WHERE ticker = \'%s\'' % (ticker)
        balMySQL = 'SELECT * FROM balance_sheet WHERE ticker = \'%s\'' % (ticker)
        
        # Get a list of date first
        cursor.execute(dateMySQL)
        fetchDate = cursor.fetchall() # After the executation we use the fetch method
        datelist = []
        for i in range(len(fetchDate)):
            datelist.append(str(fetchDate[i][0])) # fetchData[i][0] -> You get the value inside the tuple; str() -> Display the date
        
        # Secondly we check whether we have the date stored
        if date not in datelist:
            print('Missing Date.')
        else:
            
            # Then get the value of close price
            cursor.execute(priceMySQL)
            fetchPrice = cursor.fetchall()
            price = float(fetchPrice[0][0])
    
            # Get the company information    
            cursor.execute(infoMySQL)
            fetchinfo = cursor.fetchall()
            info = fetchinfo[0]
            
            # Get the balance sheet information
            cursor.execute(balMySQL)
            fetchbal = cursor.fetchall()
            balance = fetchbal[0]
            
            #------------------------------------------------------
            # From MongoDB to Python script
            # Get the company news post date
            mongodate = []
            for i in db[ticker.upper()].find({}, {"_id":0, "Posted Date":1}): # Case senditive
                mongodate.append(i)  
            
            # I need to convert the imputted date to the format aligns with MongoDB's date format
            d = datetime.strptime(date, "%Y-%m-%d")
            newdate = d.strftime('%b %d, %Y')
            
            # Check whether we have the date in MongoDB
            if {'Posted Date': newdate} not in mongodate:
                print('No news for this date.')
            else:
                for i in db[ticker.upper()].find({"Posted Date": newdate}):
                    news = i['Content']
                    news = news.replace(u'\xa0', u' ')
                
    #------------------------------------------------------
    # Return all the values
    return info, price, balance, news

# Take a try
searchData(ticker, date)


# ------------------------------------Time Series Analysis------------------------------------ #
#------------------------------------------------------
# Data Collection
# Example
ticker = 'aapl'

# SQL command
priceMySQL = 'SELECT close FROM %s' % (ticker)
dateMySQL = 'SELECT date FROM %s' % (ticker)

# Get the value of close price
cursor.execute(priceMySQL)
fetchPrice = cursor.fetchall()
closePrice = []
for i in range(len(fetchPrice)):
    closePrice.append(float(fetchPrice[i][0]))

# Get the value of date
cursor.execute(dateMySQL)
fetchDate = cursor.fetchall() # After the executation we use the fetch method
datelist = []
for i in range(len(fetchDate)):
    datelist.append(str(fetchDate[i][0])) # fetchData[i][0] -> You get the value inside the tuple; str() -> Display the date

del closePrice[-1]            
del datelist[-1]
del datelist[0]

# Get the return of the stock 
returnList = []
for i in range(1, len(closePrice)):
    returnList.append(round((closePrice[i] - closePrice[i-1])/closePrice[i-1], 5))

#------------------------------------------------------ 
# Model fitting   
# Then we merge these two lists into one new table
tablePy = pd.DataFrame({'Daily Return': returnList,
                        'Date':  datelist
                        })

# Visualize the data first
tablePy = tablePy.set_index('Date')
tablePy.plot()
plt.savefig('Daily Return for AAPL.png')
autocorrelation_plot(tablePy)

# Fit model
model = ARIMA(tablePy, order=(3,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Plot residual errors
residuals = pd.DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()
residuals.plot(kind='kde')
pyplot.show()
print(residuals.describe())
