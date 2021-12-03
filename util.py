import requests


def get_request(url, retry=0):
    try:
        print('GET {} - attempt {}'.format(url, retry))
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.exceptions.HTTPError as httperr:
        # if the GET request returns something other than 200 OK, return error to user
        if retry < 5:
            print('-HTTP Error, will retry:', httperr)
            res = get_request(url, retry + 1)
        else:
            print('-HTTP Error, not retrying', httperr)
            return None
    except requests.exceptions.Timeout as timeouterr:
        # in case of request timeout, retry the request
        if retry < 5:
            print('-Timeout Error, will retry:', timeouterr)
            res = get_request(url, retry + 1)
        else:
            print('-Timeout Error, not retrying', timeouterr)
            return None
    except requests.exceptions.TooManyRedirects as redirecterr:
        # potentially bad URL, return error to user
        print('-TooManyRedirects, potentially bad URL:', redirecterr)
        return None
    except requests.exceptions.RequestException as generalerr:
        # catastrophic error of some sort, return error to user
        print('-General Error', generalerr)
        return None

    print('Successfully pulled URL')
    return res

