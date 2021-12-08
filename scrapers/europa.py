# source page: https://webgate.ec.europa.eu/fsd/fsf/public/files/pdfFullSanctionsList/content?token=dG9rZW4tMjAxNw
# this returns a PDF which will be hard to scrape
# this link --> https://webgate.ec.europa.eu/fsd/fsf/public/files/csvFullSanctionsList/content?token=dG9rZW4tMjAxNw
#  returns CSV instead

import os
import util
from datetime import datetime


def main():
    print("CSV available from the Europa site at this link: "
          "https://webgate.ec.europa.eu/fsd/fsf/public/files/csvFullSanctionsList/content?token=dG9rZW4tMjAxNw")

    url = "https://webgate.ec.europa.eu/fsd/fsf/public/files/csvFullSanctionsList/content?token=dG9rZW4tMjAxNw"

    # now that we have our results, we need to put them into a CSV
    # first get the date in ISO format so we can organize our CSVs
    date = datetime.now()
    formattedDate = date.strftime('%Y-%m-%d')

    # create our filename for this source
    fileName = '{}_europa_sanctions.csv'.format(formattedDate)

    # point our path to the results folder, and remove the file if one has
    #  already been created with the same name
    filePath = os.path.join('results', fileName)
    if os.path.exists(filePath):
        os.remove(filePath)

    fileObj = util.get_request(url)

    with open(filePath, 'wb') as localFile:
        localFile.write(fileObj.content)

    print('results/{} created\nPLEASE NOTE: This file is semi-colon (;) delimited and not '
          'comma (,) delimited.'.format(fileName))


if __name__ == '__main__':
    main()
