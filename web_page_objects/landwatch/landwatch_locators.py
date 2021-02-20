"""Created October 17th, 2020 by Alysha Kester-Terry https://github.com/alyshakt
    This Base Page object locator strategy was gleaned with much gratitude from
    http://elementalselenium.com/tips/9-use-a-base-page-object
"""

from selenium.webdriver.common.by import By


class BasePageLocators(object):
    """Base Page Locators - Elements on EVERY page"""
    EXAMPLE_EL = (By.TAG_NAME, 'p')


class LandwatchPageLocators(object):
    """Search Page Locators"""
    GO_BTN = (By.XPATH, '//button[@text="Go"]')
    SEARCH_SECTION = (By.XPATH,'//*[@id="search"]/div/div/div/div/div')
    SEARCH_INPUT = (By.XPATH, '//*[@id="input-Search"]')
    MAX_PRICE_INPUT = (By.ID, 'priceMax')
    ADD_PRICE_BTN = (By.XPATH, '//*[@id="expansible1"]/div/div/div[3]/button')
    MIN_PARCEL_INPUT = (By.ID, 'acresMin')
    ADD_PARCEL_BTN = (By.XPATH, '//*[@id="expansible1"]/div/div/div[4]/button')
    AVAILABILITY_SECTION = (By.XPATH, '//*[@id="expansible1"]/div/fieldset')
    UNDER_CONTRACT_OP = (By.XPATH, '//a[@text="Under Contract"]')
    RESULTS_LIST = (By.XPATH, '//*[@id="root"]/div[2]/div/div[3]/div/div[2]/div[2]')
    RESULTS_PRICE = (By.XPATH, '//*[@id="root"]/div[2]/div/div[3]/div/div[2]/div[2]/div/div/a/div[contains(text(),"$")]')
    RESULTS_TEXT = (By.XPATH, '//*[@id="root"]/div[2]/div/div[3]/div/div[2]/div[2]/div/div/a/div/span')
    RESULTS_DETAIL = (By.XPATH, '//*[@id="root"]/div[2]/div/div[3]/div/div[2]/div[2]/div/div/a/p')
    RESULTS_LINK = (By.XPATH, '//*[@id="root"]/div[2]/div/div[3]/div/div[2]/div[2]/div/div[1]/a')
