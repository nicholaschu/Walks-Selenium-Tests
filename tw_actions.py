import configparser
from datetime import datetime
from enum import Enum
import os
import random
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time


class General:

    def set_up_selenium(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 60)

    def tear_down_selenium(self):
        self.browser.quit()

    def initialize_test(self, test_name: str, environment: str):
        self.test_name = test_name
        self.environment = environment
        self.parser = configparser.ConfigParser()

        self.parser.read("config.ini")

        self.url = self.parser.get(self.environment, "url")
        self.first_name = self.parser.get(self.environment, "first_name")
        self.last_name = self.parser.get(self.environment, "last_name")
        self.email = self.parser.get(self.environment, "email")
        self.phone = self.parser.get(self.environment, "phone")
        self.card_number = self.parser.get(self.environment, "card_number")
        self.expiry_month = self.parser.get(self.environment, "expiry_month")
        self.expiry_year = self.parser.get(self.environment, "expiry_year")
        self.cvv = self.parser.get(self.environment, "cvv")
        self.address = self.parser.get(self.environment, "address")
        self.country = self.parser.get(self.environment, "country")
        self.zip = self.parser.get(self.environment, "zip")
        self.state = self.parser.get(self.environment, "state")
        self.city = self.parser.get(self.environment, "city")
        self.screenshot_dir = "screenshots/" + self.environment + "/" + self.test_name

        os.makedirs(self.screenshot_dir, exist_ok=True)

    def initialize_action_chains(self):
        self.actions = ActionChains(self.browser)

    def save_screenshot(self, file_name: str):
        self.browser.save_screenshot(
            self.screenshot_dir + "/" + str(datetime.now()) + " - " + file_name + ".png")

    def focus(self, element: webdriver.remote.webelement.WebElement):
        self.browser.execute_script("arguments[0].focus();", element)

    def load_site(self):
        self.browser.get(self.url)
        assert "Take Walks" in self.browser.title

    def select_market(self):
        region = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "European Tours")))
        market = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Rome")))

        self.initialize_action_chains()
        self.save_screenshot("Pre-Market")
        self.actions.move_to_element(region).click(market).perform()
        self.save_screenshot("Post-Market")

    def select_tour(self):
        tour_overview = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.tour-list-items.vertical")))
        tours = tour_overview.find_elements_by_tag_name("a")
        tour = random.choice(tours)

        print("loading " + tour.get_attribute("href") + " ...")
        self.save_screenshot("Pre-Tour")
        tour.send_keys(Keys.ENTER)
        self.save_screenshot("Post-Tour")

    def increment_month(self):
        for i in range(2):
            next_month = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.right-book-desktop a.datepick-cmd-next")))

            next_month.click()
            time.sleep(0.25)

    def select_date(self):
        calendar = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.right-book-desktop div.datepick-month")))
        weeks = calendar.find_elements_by_tag_name("tr")
        availableDays = []

        print(len(availableDays))

        for week in weeks:
            availableDays.extend(week.find_elements_by_tag_name("a"))

            if len(availableDays) > 0:
                break

        if not availableDays:
            raise Exception("no available days two months in advance")

        self.wait.until(EC.visibility_of(availableDays[0]))
        print(availableDays[0].get_attribute("title"))
        time.sleep(0.5)
        self.save_screenshot("Pre-Date")
        availableDays[0].send_keys(Keys.ENTER)

    def select_time(self):
        time_select = Select(self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.right-book-desktop select[name="time"]'))))

        time_select.select_by_index(1)

    def select_adults(self):
        adults = Select(self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.right-book-desktop select[name="adults"]'))))

        adults.select_by_index(1)

    def book_tour(self):
        book = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.right-book-desktop button.btn-book-now")))

        self.save_screenshot("Pre-Book")
        book.send_keys(Keys.ENTER)
        self.save_screenshot("Post-Book")

    def fill_first_name(self):
        first_name = self.wait.until(
            EC.visibility_of_element_located((By.ID, "theFirstname")))

        first_name.send_keys(self.first_name)

    def fill_last_name(self):
        last_name = self.browser.find_element_by_id("theLastname")

        last_name.send_keys(self.last_name)

    def fill_email(self):
        email = self.browser.find_element_by_id("theEmail")

        email.send_keys(self.email)

    def fill_phone(self):
        phone = self.browser.find_element_by_id("thePhone")

        phone.send_keys(self.phone)
        self.save_screenshot("Post-Phone")

    def fill_credit_card(self):
        cc = self.browser.find_element_by_id("ccno")

        cc.send_keys(self.card_number)

    def select_expiry_month(self):
        cc_month = Select(self.browser.find_element_by_name("ccMonth"))

        cc_month.select_by_value(self.expiry_month)

    def select_expiry_year(self):
        cc_year = Select(self.browser.find_element_by_name("ccYear"))

        cc_year.select_by_value(self.expiry_year)

    def fill_cvv(self):
        cvv = self.browser.find_element_by_id("theCcv")

        cvv.send_keys(self.cvv)
        self.save_screenshot("Post-CVV")

    def fill_address(self):
        address = self.browser.find_element_by_name("street_address")

        address.send_keys(self.address)

    def select_country(self):
        country = Select(self.browser.find_element_by_name("country"))

        country.select_by_value(self.country)

    def fill_zip_code(self):
        zip = self.browser.find_element_by_name("zip")

        zip.send_keys(self.zip)

    def select_state(self):
        state = Select(self.browser.find_element_by_id("state_select"))

        state.select_by_value(self.state)

    def fill_city(self):
        city = self.browser.find_element_by_name("city")

        city.send_keys(self.city)

    def tick_terms_and_conditions(self):
        terms = self.browser.find_element_by_css_selector(
            'label[for="ccb_01"]')

        terms.click()

    def submit_payment_form(self):
        pay = self.browser.find_element_by_class_name("complete_booking")

        self.save_screenshot("Pre-Pay")
        pay.click()
        self.save_screenshot("Post-Pay")

        booking_confirmation = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-sub-title")))
        booking_id = "".join(re.findall(r"\d", booking_confirmation.text))

        print(self.environment + " " + booking_id + " " + self.test_name)
        self.save_screenshot("BookingConfirmation - " + booking_id + "")


class PromoCode:

    def __init__(self, general: General):
        self.browser = general.browser
        self.wait = general.wait
        self.save_screenshot = general.save_screenshot

    def fill_promo_code(self):
        promo_code_box = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "PROMO CODE")))

        self.save_screenshot("Pre-PromoBox")
        promo_code_box.send_keys(Keys.ENTER)
        self.save_screenshot("Post-PromoBox")

        promo_code = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "promo")))

        promo_code.send_keys("rc10")
        self.save_screenshot("Post-PromoCode")

        apply_promo = self.browser.find_element_by_class_name("promo-btn")

        apply_promo.send_keys(Keys.ENTER)


class Cache:

    def __init__(self, general: General):
        self.browser = general.browser
        self.wait = general.wait
        self.save_screenshot = general.save_screenshot

    def get_all_market_links(self) -> list:
        nav_bar = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.topnav-nav")))
        regions = nav_bar.find_elements_by_css_selector(
            "div[data-country-toggler]")
        all_market_links = []

        for region in regions:
            markets = region.find_elements_by_css_selector("div.inner-list a")
            market_links = [market.get_attribute("href") for market in markets]

            print(str(len(markets)) + " total markets in " +
                  region.get_attribute("data-country-toggler"))
            print(market_links)
            all_market_links.extend(market_links)

        print(str(len(all_market_links)) + " total markets in all regions")
        print(all_market_links)

        return all_market_links

    def get_tour_links_from_market(self, market_link: str) -> list:
        self.browser.get(market_link)

        tour_overview = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.tour-list-wrap")))
        tours = tour_overview.find_elements_by_css_selector(
            "div.tour-list-items a")
        tour_links = [tour.get_attribute("href") for tour in tours]

        print(str(len(tour_links)) + " total tours in " + market_link)
        print(tour_links)

        return tour_links

    def load_all_tours(self):
        market_links = self.get_all_market_links()

        for market_link in market_links:
            tour_links = self.get_tour_links_from_market(market_link)

            for tour_link in tour_links:
                print("loading " + tour_link + " ...")
                self.browser.get(tour_link)
                self.wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.right-book-desktop")))
                time.sleep(1)
                self.save_screenshot(tour_link.replace(
                    market_link, "").strip("/"))
