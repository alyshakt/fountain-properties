"""To set up the search engine environment"""


def get_app_url(SiteToScrape):
    """To define the search engine URL by type given"""
    switcher = {
        SiteToScrape.landwatch: 'https://www.landwatch.com/'
    }
    print(switcher.get(SiteToScrape, 'Invalid search site, or not yet implemented.'))
    return switcher.get(SiteToScrape)


def navigate_to_site(driver, SiteToScrape):
    """To navigate to the site URL by type given"""
    driver.get(get_app_url(SiteToScrape))
    link = driver.current_url
    print('The current url is: {}'.format(link))


def go_to_landwatch_search(driver, SiteToScrape, search_area='any', min_acreage='1', max_acreage='60',
                           max_price='10000', sortby=None):
    min_acreage = str(min_acreage)
    max_acreage = str(max_acreage)
    max_price = str(max_price)
    if sortby is None:
        sortby = 'sort-price-acres-low-high'
    elif 'htl' in sortby:
        sortby = 'sort-price-high-low'
    elif 'lth' in sortby:
        sortby = 'sort-price-low-high'
    elif 'ppal' in sortby:
        sortby = 'sort-price-acres-low-high'
    elif 'ppah' in sortby:
        sortby = 'sort-price-acres-high-low'
    elif 'lts' in sortby:
        sortby = 'sort-acres-high-low'
    driver.get(get_app_url(SiteToScrape.landwatch))
    link = driver.current_url
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
    final_url = new_url + '/price-1000-' + max_price + '/acres-' + min_acreage + '-' + max_acreage + '/available/' + sortby
    print(final_url)
    driver.get(final_url)
