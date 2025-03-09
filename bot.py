from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import pandas as pd
import time


df = pd.read_excel("C:/Users/agam1/OneDrive/Desktop/gog_games.xlsx")


driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/login")
time.sleep(3)


driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("admin123")

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.TAG_NAME, "button"))
)
login_button.click()
time.sleep(3)

driver.find_element(By.XPATH, "//button[contains(text(), 'Add Game')]").click()
time.sleep(2)

for index, row in df.iterrows():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "game-title"))).clear()
    driver.find_element(By.ID, "game-title").send_keys(row["title"])

    driver.find_element(By.ID, "game-genre").clear()
    driver.find_element(By.ID, "game-genre").send_keys(row["genre"])

    driver.find_element(By.ID, "game-price").clear()
    driver.find_element(By.ID, "game-price").send_keys(int(float(row["price"].replace("$", "").strip())))

    driver.find_element(By.ID, "game-quantity").clear()
    driver.find_element(By.ID, "game-quantity").send_keys(str(row["quantity"]))

    add_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add Game')]")
    add_button.click()

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()
    except:
        print(f"✅ Game '{row['title']}' added without an alert.")

    time.sleep(2)

driver.quit()
print("✅ All games added successfully!")
