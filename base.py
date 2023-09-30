from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle
import selenium.webdriver.common.keys as keys

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # You'll need to provide the path to your Chrome WebDriver executable
wait = WebDriverWait(driver, 10)  # Set a WebDriverWait with a timeout of 10 seconds

# Open the website
driver.get("https://zho.gov.ae/ar-AE/Sign-Language-Dictionary/UAE-Sign-Language-Categories/Arabic-Sign-Languages#mastercard_categoryname=%D8%A7%D9%84%D8%B3%D9%85%D8%A7%D8%AA%20%D9%88%D8%A7%D9%84%D9%85%D9%88%D8%A7%D9%82%D9%81")  # Replace with the URL of the website you want to interact with
fn = 'vid data-c3.pickle'
time.sleep(6)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight-3500);")

while True:
    try:
        # Wait for the "LOAD MORE" button to become present
        load_more_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="button" and @value="تحميل المزيد"]'))
        )
        
        # Scroll to the "LOAD MORE" button to make it visible
        actions = ActionChains(driver)
        actions.move_to_element(load_more_button).perform()
        
        # Wait for the button to become clickable again
        load_more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="تحميل المزيد"]'))
        )
        
        # Click the "LOAD MORE" button
        load_more_button.click()
        
        # Wait for the page to load completely (you may need to adjust the conditions here)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='content']")))
            
    except ElementNotInteractableException:
        break
    except Exception as e:
        print(e)
        # If the "LOAD MORE" button is not found, break out of the loop
        pass


# Locate the <ul> element with class "search-result-list"
list_element = driver.find_element(By.CLASS_NAME, "search-result-list")

# Locate the first <li> element within the <ul> (assuming it's the first item you want to click)
first_item = list_element.find_element(By.TAG_NAME, "li")

# Click on the first item
first_item.click()

time.sleep(4)
data = {}
while True:
    try:
        time.sleep(1)
        try:
            download_link = driver.find_element(By.XPATH, "//a[contains(text(), 'تحميل الفيديو')]")
        except:
            download_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
        # Extract the href attribute value
        href_value = download_link.get_attribute("href")

            # Locate the <h4> element
        h4_element = driver.find_element(By.XPATH, "//h4[contains(@class,'truncate')]")

        # Extract the text inside the <h4> element
        h4_text = h4_element.text

        print(h4_text, href_value)
        data[h4_text] = href_value

        with open(fn, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


        action = ActionChains(driver)
        action.send_keys(keys.Keys.ARROW_RIGHT).perform()

        time.sleep(1.5)
    except Exception as e:
        print(e)

    
    


