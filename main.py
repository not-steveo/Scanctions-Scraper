import os

from scrapers import cbp
from scrapers import dol
from scrapers import europa
from scrapers import ica
from scrapers import treasury


def main():

    # create results folder if it doesn't exist
    currPath = os.getcwd()
    resultsPath = os.path.join(currPath, "results")
    exists = os.path.exists(resultsPath)
    if not exists:
        os.makedirs(resultsPath)
        print("/results directory created\n")

    # run the individual scrapers
    print("Running the Customs and Border Patrol scraper...")
    cbp.main()
    print("\nRunning the Department of Labor scraper...")
    dol.main()
    print("\nRunning the Europa scraper...")
    europa.main()
    print("\nRunning the International Cotton Association scraper...")
    ica.main()
    print("\nRunning the Treasury SDN List scraper...")
    treasury.main()


if __name__ == '__main__':
    main()
