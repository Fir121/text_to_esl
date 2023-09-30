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
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Open the website
driver.get("https://zho.gov.ae/ar-AE/Sign-Language-Dictionary/UAE-Sign-Language-Categories/Arabic-Sign-Languages")
fn = 'vid data.pickle'
time.sleep(6)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight-3500);")

while True:
    try:
        load_more_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="button" and @value="تحميل المزيد"]'))
        )
        
        actions = ActionChains(driver)
        actions.move_to_element(load_more_button).perform()
        
        load_more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="تحميل المزيد"]'))
        )
        
        load_more_button.click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='content']")))
            
    except ElementNotInteractableException:
        break
    except Exception as e:
        print(e)
        pass


list_element = driver.find_element(By.CLASS_NAME, "search-result-list")

first_item = list_element.find_element(By.TAG_NAME, "li")

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

        h4_element = driver.find_element(By.XPATH, "//h4[contains(@class,'truncate')]")

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

        action = ActionChains(driver)
        action.send_keys(keys.Keys.ARROW_RIGHT).perform()

        continue

    
    


