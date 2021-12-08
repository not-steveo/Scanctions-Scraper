# scrape the table on this page: https://www.treasury.gov/ofac/downloads/sdnlist.txt
# output to CSV

import os
import util
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://www.treasury.gov/ofac/downloads/sdnlist.txt"

    # temporarily storing the scraped data in a Dictionary object that will be converted
    #  to a CSV at the end of our scraping
    # {count: [countryName, company, town, awardDate, listingDate]}
    resultsDict = {}

    # use our custom get function to fetch the page
    page = util.get_request(url)

    # make sure a page was returned, if the request failed for some reason we don't want the script to crash
    if page is not None:

        # this page is just a txt file, no need for beautifulsoup
        # we will just process the text as text
        entries = page.text.split('\n\n')

        # iterate over entries, skip first one and last 4 (just informational stuff)
        count = 0
        for entry in entries[1:-4]:

            if "~(" not in entry:
                entity = ""  # name of individual or company
                type = ""  # "individual", "vessel", "aircraft"
                tags = []  # the value in each entry in []
                tagString = ""
                linkedTo = ""

                entry = entry.replace('\n', ' ')

                tagParts = entry.split('[')

                entity = tagParts[0].strip()

                # skip first item in list
                for tagPart in tagParts[1:]:
                    if "(" in tagPart:
                        # split on close bracket ]
                        # take first list item for tag part
                        # check if second list item is "Linked To" string and process if so

                        moreParts = tagPart.split(']')

                        firstPart = moreParts[0]
                        firstPart = firstPart.replace(' ', '')

                        tags.append(firstPart.strip())  # first item in list will be our tag

                        # second item will be the string containing the Linked To: info
                        # due to a lack of standardization, we process text with individual replace statements
                        # these statements should work for all variations that we see around this info
                        if "Linked" in moreParts[1]:
                            processString = moreParts[1]
                            processString = processString.replace(')', '')
                            processString = processString.replace('(', '')
                            processString = processString.replace('.', '')
                            processString = processString.replace('Linked To:', '')
                            processString = processString.replace(' ', '', 2)
                            linkedTo = processString.strip()
                    else:
                        # remove close bracket and space
                        # add to list of tags
                        tagPart = tagPart.replace(']', '')
                        tagPart = tagPart.replace(' ', '')
                        tagPart = tagPart.replace('.', '')
                        tags.append(tagPart.strip())

                if len(tags) > 0:
                    tagString = '; '.join(tags)

                # cheap and easy way to find type
                indivCheck = entity.replace(" (individual)", '')
                if len(indivCheck) != len(entity):
                    type = "individual"
                    entity = indivCheck.strip()

                aircraftCheck = entity.replace(" (aircraft)", '')
                if len(aircraftCheck) != len(entity):
                    type = "aircraft"
                    entity = aircraftCheck.strip()

                vesselCheck = entity.replace(" (vessel)", '')
                if len(aircraftCheck) != len(entity):
                    type = "vessel"
                    entity = vesselCheck.strip()

                # some final processing to make sure no rouge commas interfere with our CSV and there's not excessive ""
                entity = entity.replace(',', ';')
                entity = entity.replace('"""""', '"')
                entity = entity.replace('""""', '"')
                entity = entity.replace('"""', '"')
                entity = entity.replace('""', '"')
                entity = entity.replace('"""\'', '"')
                tagString = tagString.replace(',', ';')
                linkedTo = linkedTo.replace(',', ';')

                resultsDict[count] = [entity, type, tagString, linkedTo]
                count += 1

        # now that we have our results, we need to put them into a CSV
        # first get the date in ISO format so we can organize our CSVs
        date = datetime.now()
        formattedDate = date.strftime('%Y-%m-%d')

        # create our filename for this source
        fileName = '{}_treasury_sdn_list.csv'.format(formattedDate)

        # point our path to the results folder, and remove the file if one has
        #  already been created with the same name
        filePath = os.path.join('..', 'results', fileName)
        if os.path.exists(filePath):
            os.remove(filePath)

        # create a pandas DataFrame from our dictionary
        df = pd.DataFrame.from_dict(resultsDict, orient='index')
        # name the columns that we'll want in the CSV
        df.columns = ['Entity', 'Type', 'Tags', 'Linked To']
        # sort alphabetically
        df = df.sort_values(by=['Entity', 'Type'])
        # output to CSV
        df.to_csv(filePath, index=False)
        print('{} created\n'.format(fileName))


if __name__ == "__main__":
    main()


