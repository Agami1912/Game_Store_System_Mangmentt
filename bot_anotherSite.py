import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start the WebDriver
driver = webdriver.Chrome()

# Open the GOG website
driver.get("https://www.gog.com/en/games")

# Allow JavaScript elements to load
time.sleep(5)  # Wait to ensure initial elements are loaded

# Scroll down multiple times to load more games (GOG uses lazy loading)
for _ in range(10):  # Increased scroll times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new content to load

# Wait for game elements to be visible
wait = WebDriverWait(driver, 15)
game_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-tile")))

game_data = []

for game in game_elements:
    try:
        # Extract title
        title_element = game.find_element(By.CLASS_NAME, "product-tile__title")
        title = title_element.text.strip()

        # Extract price - Handle different cases
        try:
            # Case 1: Discounted Price
            price_element = game.find_element(By.CLASS_NAME, "final-value")
            price = price_element.text.strip()
        except:
            try:
                # Case 2: Regular Price
                price_element = game.find_element(By.CLASS_NAME, "product-tile__price")
                price = price_element.text.strip()
            except:
                # Case 3: Free Game
                price = 0

        # Extract genre (GOG does not store genre in 'data-genre')
        try:
            genre_element = game.find_element(By.CLASS_NAME, "product-tile__tags")
            genre = genre_element.text.strip()
        except:
            genre = "N/A"

        # Append data
        game_data.append({
            "title": title,
            "genre": genre,
            "price": price,
            "quantity": 1
        })
    except Exception as e:
        print(f"Error extracting data: {e}")

# Save data to Excel
df = pd.DataFrame(game_data)
df.to_excel("C:/Users/agam1/OneDrive/Desktop/gog_games.xlsx", index=False, engine='openpyxl')

# Close the browser
driver.quit()

print("✅ Data saved to gog_games.xlsx")
