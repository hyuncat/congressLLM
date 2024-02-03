import requests
from bs4 import BeautifulSoup
import os
# from datetime import datetime

# Get links to recent legislation, if further info is needed
# https://www.senate.gov/pagelayout/legislative/b_three_sections_with_teasers/active_leg_page.htm 

SENATE = "s"
HOUSE = "h"

# Type can be s (senate), h (house) (can be changed)
def get_bill_summary_link(type, n):
    # We can either automate changing of congress number or just manually since it won't change for another year
    base_url = "https://www.congress.gov/bill/118th-congress/"
    if type == SENATE:
        base_url += "senate"
    elif type == HOUSE:
        base_url += "house"
    base_url += "-bill/" + str(n)

    return base_url

print(get_bill_summary_link("s", 2226))
