"""To set up the search engine environment"""


def get_app_url(SiteToScrape):
    """To define the search engine URL by type given"""
    switcher = {
        SiteToScrape.landwatch: 'https://www.landwatch.com/'
    }
    print(switcher.get(SiteToScrape, 'Invalid search site, or not yet implemented.'))
    return switcher.get(SiteToScrape)


def navigate_to_site(driver, SiteToScrape, search_area='any'):
    """To navigate to the site URL by type given"""
    driver.get(get_app_url(SiteToScrape))
    link = driver.current_url
    print('The current url is: {}'.format(link))
    new_url = None
    if 'landwatch' in str(link):
        if 'az' in search_area:
            new_url = link + 'arizona-land-for-sale/'
        elif 'nv' in search_area:
            new_url = link + 'nevada-land-for-sale/'
        elif 'ut' in search_area:
            new_url = link + 'utah-land-for-sale/'
        elif 'nm' in search_area:
            new_url = link + 'new-mexico-land-for-sale/'
        elif 'ca' in search_area:
            new_url = link + 'california-land-for-sale/'
        else:
            new_url = link + 'land'
        driver.get(new_url + '/price-under-10000/acres-over-5/available/sort-price-acres-low-high')
