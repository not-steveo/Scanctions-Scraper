# scrape the table on this page: https://ica-ltd.org/safe-trading/list-of-unfulfilled-awards
# print URL - https://ica-ltd.org/safe-trading/list-of-unfulfilled-awards/?pr=true
# output to CSV

import os
import util
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://ica-ltd.org/safe-trading/list-of-unfulfilled-awards/?pr=true"

    # temporarily storing the scraped data in a Dictionary object that will be converted
    #  to a CSV at the end of our scraping
    # {count: [countryName, company, town, awardDate, listingDate]}
    resultsDict = {}

    # use our custom get function to fetch the page
    page = util.get_request(url)

    # make sure a page was returned, if the request failed for some reason we don't want the script to crash
    if page is not None:
        # create the soup from the page content
        soup = BeautifulSoup(page.content, "html.parser")

        # find each line, each line is an entry of data that we need
        rows = soup.find_all('li')

        # iterate over the rows to process the data
        count = 0
        for row in rows:
            # initialize values
            country = ""
            company = ""
            city = ""
            awardDate = ""
            listingDate = ""

            # each row contains the specific data we need in divs using the class below
            details = row.find_all('div', class_="search-results__loua-cell")

            country = details[0].text.strip()
            company = details[1].text.strip()
            city = details[2].text.strip()

            # not all entries have dates so using try/accept to catch potential errors
            try:
                awardDate = details[3].text.strip()
                listingDate = details[4].text.strip()
            except IndexError:
                awardDate = ""
                listingDate = ""

            # now we need to remove the labels from the data
            # remove 'Country: ' - 9 spaces
            nCountry = country[9:]
            # remove 'Company: ' - 9 spaces
            nCompany = company[9:]
            # remove 'Town/Province: ' - 14 spaces
            nCity = city[14:]
            # remove 'Award Date:' - 11 spaces
            if len(awardDate) > 0:
                nAwardDate = awardDate[11:]
            else:
                nAwardDate = ""
            # remove 'Listing Date:' - 13 spaces
            if len(listingDate) > 0:
                nListingDate = listingDate[13:]
            else:
                nListingDate = ""

            # {count: [countryName, company, town, awardDate, listingDate]}
            resultsDict[count] = [nCountry, nCompany, nCity, nAwardDate, nListingDate]

            count += 1

        # now that we have our results, we need to put them into a CSV
        # first get the date in ISO format so we can organize our CSVs
        date = datetime.now()
        formattedDate = date.strftime('%Y-%m-%d')

        # create our filename for this source
        fileName = '{}_intnl_cotton_assoc.csv'.format(formattedDate)

        # point our path to the results folder, and remove the file if one has
        #  already been created with the same name
        filePath = os.path.join('results', fileName)
        if os.path.exists(filePath):
            os.remove(filePath)

        # create a pandas DataFrame from our dictionary
        df = pd.DataFrame.from_dict(resultsDict, orient='index')
        # name the columns that we'll want in the CSV
        df.columns = ['Country', 'Company', 'Town/Province', 'Award Date', 'Listing Date']
        # sort alphabetically
        df = df.sort_values(by=['Country', 'Company'])
        # output to CSV
        df.to_csv(filePath, index=False)
        print('results/{} created'.format(fileName))


if __name__ == "__main__":
    main()
