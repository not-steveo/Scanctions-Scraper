# scrape the table on this page: https://www.dol.gov/agencies/ilab/reports/child-labor/list-of-goods
# print URL - https://www.dol.gov/agencies/ilab/reports/child-labor/list-of-goods-print
# output to CSV

import os
import util
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://www.dol.gov/agencies/ilab/reports/child-labor/list-of-goods-print"

    # temporarily storing the scraped data in a Dictionary object that will be converted
    #  to a CSV at the end of our scraping
    # {count: [countryName, goodName, childLaborT/F, forcedLaborT/F]}
    resultsDict = {}

    # use our custom get function to fetch the page
    page = util.get_request(url)

    # make sure a page was returned, if the request failed for some reason we don't want the script to crash
    if page is not None:
        # create the soup from the page content
        soup = BeautifulSoup(page.content, "html.parser")

        # find each table row - each row contains three 'td' column values
        rows = soup.find_all('tr')

        # iterate over the rows to process the data (skip the first row, these are headers which we'll add later)
        count = 0
        for row in rows[1:]:
            # this creates a list with three objects
            cols = row.find_all('td')
            # first object is the country name, easy to get
            countryName = cols[0].text.strip()
            # some goods have descriptions that we don't want, but the specific good name is in <strong> tags so
            #  we grab just that tag
            goodName = cols[1].find('strong').text.strip()
            # if the item has a summary included, we need to include that
            summary = ""
            summaryText = cols[1].text.strip()
            if len(summaryText) > len(goodName):
                summary = summaryText[len(goodName):]
            # third object is the labor type
            laborType = cols[2].text.strip()
            # default these to False
            childLabor = False
            forcedLabor = False

            # if these values are found in that third column, set them to true
            if "Child Labor" in laborType:
                childLabor = True
            if "Forced Labor" in laborType:
                forcedLabor = True

            # throw all our results into our dictionary
            resultsDict[count] = [countryName, goodName, childLabor, forcedLabor, summary]
            count += 1

        # now that we have our results, we need to put them into a CSV
        # first get the date in ISO format so we can organize our CSVs
        date = datetime.now()
        formattedDate = date.strftime('%Y-%m-%d')

        # create our filename for this source
        fileName = '{}_dept_of_labor.csv'.format(formattedDate)

        # point our path to the results folder, and remove the file if one has
        #  already been created with the same name
        filePath = os.path.join('..', 'results', fileName)
        if os.path.exists(filePath):
            os.remove(filePath)

        # create a pandas DataFrame from our dictionary
        df = pd.DataFrame.from_dict(resultsDict, orient='index')
        # name the columns that we'll want in the CSV
        df.columns = ['Country/Area', 'Good', 'Child Labor', 'Forced Labor', 'Good Description']
        # sort alphabetically
        df = df.sort_values(by=['Country/Area', 'Good'])
        # output to CSV
        df.to_csv(filePath, index=False)
        print('{} created\n'.format(fileName))


if __name__ == "__main__":
    main()
