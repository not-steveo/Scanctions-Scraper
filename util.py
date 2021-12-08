import requests


def get_request(url, retry=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    try:
        print('GET {} - attempt {}'.format(url, retry))
        res = requests.get(url, timeout=10, headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as httperr:
        # if the GET request returns something other than 200 OK, return error to user
        if retry < 5:
            print('-HTTP Error, will retry:', httperr)
            res = get_request(url, retry + 1)
        else:
            print('-HTTP Error, not retrying', httperr)
            res = None
    except requests.exceptions.Timeout as timeouterr:
        # in case of request timeout, retry the request
        if retry < 5:
            print('-Timeout Error, will retry:', timeouterr)
            res = get_request(url, retry + 1)
        else:
            print('-Timeout Error, not retrying', timeouterr)
            res = None
    except requests.exceptions.TooManyRedirects as redirecterr:
        # potentially bad URL, return error to user
        print('-TooManyRedirects, potentially bad URL:', redirecterr)
        res = None
    except requests.exceptions.RequestException as generalerr:
        # catastrophic error of some sort, return error to user
        print('-General Error', generalerr)
        res = None

    if res is not None:
        print('Successfully pulled URL')

    return res

