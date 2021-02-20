"""Created October 17th, 2020 by Alysha Kester-Terry https://github.com/alyshakt
"""
import datetime
import time
from functools import reduce

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from web_page_objects.landwatch.landwatch_locators import LandwatchPageLocators


class BasePage(object):
    """Base class to initialize the page class that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, name=None):
        created_date = str(datetime.datetime.utcnow().strftime("%m-%d-%H%M"))
        add_name = str(name).replace(' ', '')
        file_name = 'test-reports/screenshots/' + add_name + created_date + '.png'
        self.driver.save_screenshot(file_name)

    # Expected Conditions
    def wait_for_element_visibility(self, by_locator, timeout=45):
        """Wait for an element to be visible"""
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(by_locator))

    def wait_for_element_invisibility(self, by_locator, timeout=10):
        """Wait for an element to no longer be visible"""
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(by_locator))

    # Functional/Interaction with Page Elements
    def enter_text(self, by_locator, text_to_enter):
        """Enter text into an element by a defined locator"""
        element = self.driver.find_element(*by_locator)
        element.clear()
        element.send_keys(text_to_enter + Keys.RETURN)

    def get_element_text(self, by_locator):
        """Get an element's text by a defined locator"""
        self.wait_for_element_visibility(by_locator)
        element = self.driver.find_element(*by_locator)
        return element.text

    def scroll_to_element(self, by_locator):
        element = self.driver.find_element(*by_locator)
        coordinates = element.location_once_scrolled_into_view  # returns dict of X, Y coordinates
        self.driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

    def click_element(self, by_locator):
        """Click an element by a defined locator"""
        self.wait_for_element_visibility(by_locator)
        element = self.driver.find_element(*by_locator)
        element.click()

    def wait_for_seconds(self, seconds_to_wait=10):
        time.sleep(seconds_to_wait)

    def get_page_src_info(self):
        source_hierarchy = self.driver.page_source
        return str(source_hierarchy)

    def process_failure(self, error):
        print(self.get_page_src_info())
        pytest.fail('The test failed. {}'.format(error), True)

    def tear_down(self, failure):
        if failure is None:
            self.take_screenshot('Pass')
        else:
            self.take_screenshot('Failed')
        self.driver.quit()


def calculate_average_acres(result_list):
    acres_list = list()
    result_count = len(result_list)
    for result in result_list:
        acres_list.append(int(result['listing']['acres']))
    return reduce(lambda a, b: a + b, acres_list) / result_count


def calculate_average_price(result_list):
    price_list = list()
    result_count = len(result_list)
    for result in result_list:
        price_list.append(int(result['listing']['price']))
    return reduce(lambda a, b: a + b, price_list) / result_count


class LandwatchSearchPage(BasePage):
    """Main Search Page Action Methods"""

    def quick_search(self, search_text, price, acres):
        self.wait_for_seconds(5)
        self.enter_search_area(search_text)
        self.enter_max_price(price)
        self.enter_min_acres(acres)
        self.click_go()

    def enter_search_area(self, search_text):
        self.click_element(LandwatchPageLocators.SEARCH_SECTION)
        self.wait_for_seconds(1)
        self.enter_text(LandwatchPageLocators.SEARCH_SECTION, search_text)
        self.wait_for_seconds(2)

    def enter_max_price(self, price):
        print('Entering max price: {}'.format(price))
        self.enter_text(LandwatchPageLocators.MAX_PRICE_INPUT, price)

    def enter_min_acres(self, acres):
        print('Entering min acres: {}'.format(acres))
        self.enter_text(LandwatchPageLocators.MIN_PARCEL_INPUT, acres)

    def remove_under_contract(self):
        self.scroll_to_element(LandwatchPageLocators.UNDER_CONTRACT_OP)
        self.click_element(LandwatchPageLocators.UNDER_CONTRACT_OP)

    def click_go(self):
        self.scroll_to_element(LandwatchPageLocators.GO_BTN)
        self.click_element(LandwatchPageLocators.GO_BTN)
        self.wait_for_seconds(5)

    def get_results_list(self):
        """Get a list of all the results"""
        self.wait_for_element_visibility(LandwatchPageLocators.RESULTS_LIST)
        results_text = self.driver.find_elements(*LandwatchPageLocators.RESULTS_TEXT)
        results_price = self.driver.find_elements(*LandwatchPageLocators.RESULTS_PRICE)

        results_list = list()

        for price in results_price:
            for desc in results_text:
                results_list.append('{}'.format(price.text + ' ' + desc.text))
        return results_list

    def get_results_json(self):
        self.wait_for_element_visibility(LandwatchPageLocators.RESULTS_LIST)
        results_text = self.driver.find_elements(*LandwatchPageLocators.RESULTS_TEXT)
        results_price = self.driver.find_elements(*LandwatchPageLocators.RESULTS_PRICE)
        results_links = self.driver.find_elements(*LandwatchPageLocators.RESULTS_LINK)
        results_detail = self.driver.find_elements(*LandwatchPageLocators.RESULTS_DETAIL)
        results_dict = []
        print('There are {} descriptions, {} prices and {} links '.format(len(results_text), len(results_price),
                                                                          len(results_links)))
        for i in range(len(results_price)):
            # Get Price
            price = results_price[i]
            float_price = float(price.text.replace('$', '').replace(',', '').replace('.', ''))
            # Get Description
            desc = results_text[i]
            prep_text = desc.text
            description = prep_text.split(' - ')
            acres = float(description[0].replace(' acres', ''))
            total_location = description[1]
            city_state_county = total_location.split(' (')
            city_state = city_state_county[0]
            county = city_state_county[1].replace('(', '').replace(')', '')
            # Get Details
            try:
                detail = results_detail[i]
                detail_text = detail.text.lower()
            except BaseException:
                detail_text = None
            # Get Link
            link = results_links[i]
            link_text = link.get_attribute('href')
            results_dict.append(
                {"listing": {"price": float_price, "acres": acres, "location": city_state, "county": county,
                             "detail": detail_text,
                             "link": link_text}})
            i += 1
        print('{}'.format(results_dict))
        return results_dict

    def get_optimal_results(self, wanted_county=None):
        result_list = self.get_results_json()
        to_return_list = list()
        average_price = calculate_average_price(result_list)
        print('The average price is: {}'.format(average_price))
        average_acreage = calculate_average_acres(result_list)
        print('The average acreage is: {}'.format(average_acreage))
        for result in result_list:
            this_listing = result['listing']
            acreage = this_listing['acres']
            pricing = this_listing['price']
            detail = this_listing['detail']
            county = this_listing['county'].lower()
            if acreage >= average_acreage and pricing <= average_price:
                print('This listing has more than average acreage at less than average cost: {}'.format(this_listing))
                if wanted_county is not None and wanted_county.lower() in county:
                    if detail is None or 'mining' not in detail:
                        to_return_list.append(result)
                else:
                    if detail is None or 'mining' not in detail:
                        to_return_list.append(result)
            if to_return_list is None:
                print('There are no optimal parcels! Too bad.')
        return to_return_list
