import re

def get_nextpage_id(url):
    next_id = ""
    try:
        next_id = re.search("until=(\d+)", url).group(1)
    except:
        pass

    return next_id
