# scrape the table on this page: https://www.cbp.gov/trade/forced-labor/withhold-release-orders-and-findings
# output to CSV

import os
import util
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://www.cbp.gov/trade/forced-labor/withhold-release-orders-and-findings"
    urlPrefix = "https://www.cbp.gov"

    # temporarily storing the scraped data in a Dictionary object that will be converted
    #  to a CSV at the end of our scraping
    # {count: [type(Witholding/Finding), countryName, #, Date, Merchandise, Manufacturer(s), Status]}
    resultsDict = {}

    # use our custom get function to fetch the page
    page = util.get_request(url)

    # make sure a page was returned, if the request failed for some reason we don't want the script to crash
    if page is not None:
        # create the soup from the page content
        soup = BeautifulSoup(page.content, "html.parser")

        # get country name from the headers of the panel
        countryNames = []
        headers = soup.find_all('h4', class_='panel-title')
        for header in headers:
            countryNames.append(header.text.strip())

        # get all table objects - these contain the info we need to parse out
        tables = soup.find_all('table')
        count = 0
        for i in range(len(tables)):
            table = tables[i]
            # initializing variables so that if a value isn't found, we won't run in to issues when we
            #  parse out to a CSV
            type = ""
            countryName = ""
            number = 0
            date = ""
            merchandise = ""
            manufacturer = ""
            status = ""
            statusNotes = ""
            links = ""

            # start parsing data from tables
            # from summary we should be able to get 'type' and 'countryName'
            try:
                summary = table.attrs.get('summary')
            except:
                summary = None
            # 'summary' example: "Detention Orders for Brazil"
            summaryParts = summary.split(' ')
            type = summaryParts[0]
            # countryName = summaryParts[-1]
            countryName = countryNames[i]  # summaries inconsistent, better to pull name from headers

            print(type, '-', countryName)

            # now we pull data from the rows of the table
            # skip the first two rows as they're just headers
            rows = table.find_all('tr')
            for row in rows[2:]:
                # grab all the column values and polish them up
                cols = row.find_all('td')
                values = []
                for col in cols:
                    values.append(col.text.strip())
                # values is now a list that goes in this order:
                # --> #, Date, Merchandise, Manufacturer(s), Status, Status Notes
                # parse these values out to our variables
                try:
                    number = values[0].replace(',', '')
                    date = values[1].replace(',', '')
                    merchandise = values[2].replace(',', '')
                    manufacturer = values[3].replace(',', '')
                    status = values[4].replace(',', '')
                    statusNotes = values[5].replace(',', '')
                except IndexError:
                    print('IndexError for this row:', row)

                # next we need to find any links that might be in the row
                foundLinks = []
                rawLinks = row.find_all('a')
                for link in rawLinks:
                    if 'href' in link.attrs:
                        concatLink = '{}{}'.format(urlPrefix, link.attrs.get('href'))
                        foundLinks.append(concatLink)
                if len(foundLinks) > 0:
                    links = '; '.join(foundLinks)

                if len(merchandise) > 0:
                    resultsDict[count] = [type, countryName, number, date, merchandise,
                                          manufacturer, status, statusNotes, links]
                count += 1

        # now that we have our results, we need to put them into a CSV
        # first get the date in ISO format so we can organize our CSVs
        date = datetime.now()
        formattedDate = date.strftime('%Y-%m-%d')

        # create our filename for this source
        fileName = '{}_us_customs_and_border_protection.csv'.format(formattedDate)

        # point our path to the results folder, and remove the file if one has
        #  already been created with the same name
        filePath = os.path.join('..', 'results', fileName)
        if os.path.exists(filePath):
            os.remove(filePath)

        # create a pandas DataFrame from our dictionary
        df = pd.DataFrame.from_dict(resultsDict, orient='index')
        # name the columns that we'll want in the CSV
        df.columns = ['Type', 'Country', '#', 'Date', 'Merchandise', 'Manufacturer(s)', 'Status', 'Status Notes', 'Links']
        # sort alphabetically
        df = df.sort_values(by=['Type', 'Country', '#'])
        # output to CSV
        df.to_csv(filePath, index=False)
        print('{} created\n'.format(fileName))


if __name__ == "__main__":
    main()

