
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

url = "https://orteil.dashnet.org/cookieclicker/"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Function to click the "consent" button automatically
def consent_dashnet_data():
    try:
        # Wait for the consent button to be clickable
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p"))
        )
        consent_button.click()
    except TimeoutException:
        print("Consent button not found within the time limit")
    except ElementClickInterceptedException as e:
        print(f"Click intercepted: {e}")
        # Handle the interception by trying to click again after making sure the overlay is interactable
        try:
            overlay_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]"))
            )
            # Ensure the overlay is interactable
            driver.execute_script("arguments[0].style.visibility='visible';", overlay_element)
            consent_button.click()
        except TimeoutException:
            print("Overlay element not found within the time limit")
        except Exception as e:
            print(f"Failed to handle overlay: {e}")

# Function to select English automatically
def select_language():
    try:
        # Wait for the language selection button to be clickable
        lang_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="langSelect-EN"]'))
        )
        lang_button.click()
    except TimeoutException:
        print("Language selection button not found within the time limit")
    except ElementClickInterceptedException as e:
        print(f"Click intercepted: {e}")

# open up the website to where it can be played
consent_dashnet_data()
select_language()

# starts playing the game
def click_cookie():
    while True:
        try:
            # Wait for the big cookie button to be clickable
            big_cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'bigCookie'))
            )
            big_cookie_button.click()
            break  # Break the loop if click is successful
        except (TimeoutException, StaleElementReferenceException):
            print("Retrying big cookie button click due to Timeout or StaleElementReferenceException")
        except ElementClickInterceptedException as e:
            print(f"Click intercepted: {e}")


def find_unlocked_products():
    return driver.find_elements(By.XPATH, value='//*[@class="product unlocked enabled"]')

def buy_product(product):
    product.click()
    

# Timer setup for playing game
start_time = time.time()
buy_time = start_time
elapsed_time = 0
buy_interval = 0.5
game_duration = 300

while elapsed_time < game_duration:
    
    click_cookie()

    # update elapsed time
    current_time = time.time()
    elapsed_time = current_time-start_time

    # check for new item, increases by 20% after every purchase
    if current_time - buy_time >=buy_interval:
        print(buy_interval)
        try:
            buy_product(find_unlocked_products()[-1])
        except IndexError:
            pass
        buy_time = current_time
        buy_interval *= 1.2




