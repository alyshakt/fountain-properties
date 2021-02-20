"""Created October 17th, 2020 by Alysha Kester-Terry https://github.com/alyshakt"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from setup_helpers import screenshots, web_app_setup
from setup_helpers.SiteToScrape import SiteToScrape
from web_page_objects.landwatch.landwatch_pages import BasePage, LandwatchSearchPage


def test_all_under_10k(record_xml_attribute):
    """prop-types-4132/price-under-10000/acres-over-1/available/sort-price-low-high
    Land in Arizona with > 1 acre with price < 10k
    """
    record_xml_attribute(
        'name', 'Any Land > 5 acres with price < 10k')
    fail = None
    # Setup Driver, define options
    options = FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    # Define the SearchEngineType and the page object
    web_app_setup.go_to_landwatch_search(driver, SiteToScrape.landwatch, search_area='any', min_acreage=5,
                                         max_price=10000)
    search_page = LandwatchSearchPage(driver)
    base_page = BasePage(driver)

    # I recommend beginning with a try-catch-finally format
    try:
        # Get a results list and iterate through it looking for your search terms
        # Take a screenshot
        optimal_results_list = search_page.get_optimal_results()
        screenshots.take_screenshot(driver, 'All Land')
        print('We found {} optimal listings to consider {}:'.format(len(optimal_results_list), optimal_results_list))
        search_page.write_to_csv('test-reports/ANY_GT5ACRES_LT10k.csv', optimal_results_list)
    except (BaseException, Exception) as failure:
        fail = failure
        print('!!!!! The test failed. {}'.format(fail))
        base_page.process_failure(fail)
    finally:
        # Finally, quit the driver and appium service!
        base_page.tear_down(fail)
