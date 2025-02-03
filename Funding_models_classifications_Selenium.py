import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to ChromeDriver
chromedriver_path = "Path to ChromeDriver"

# Chrome profile path
chrome_profile_path = "your profile path"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={chrome_profile_path}")  # Use existing profile
chrome_options.add_argument("--profile-directory=Default")  # Default profile
chrome_options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
)

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

# Maximize browser window
driver.maximize_window()

# Open ChatGPT
try:
    print("Opening ChatGPT...")
    driver.get("https://chat.openai.com/")

    # Wait for CAPTCHA or login screen
    print("Please resolve the CAPTCHA manually if prompted.")
    time.sleep(60)  # Wait for manual CAPTCHA resolution and login

    # Verify login success
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Send a message']"))
    )
    print("Login successful!")

    # Read Excel input file
    input_file = "your input excel file path"
    df = pd.read_excel(input_file)

    # Process each project
    results = []
    for _, row in df.iterrows():
        project_name = row.iloc[0]
        github_link = row.iloc[1]

        prompt = f"""Please classify the project's funding model based on its GitHub repository, white paper, CoinMarketCap, and official website (if available). 
        Respond in the following format (include only applicable funding models):
        - Public Token Sale: [Yes/No]
        - Product/Service Sales Income: [Yes/No]
        - Donations: [Yes/No]
        - Crowdfunding Without Token: [Yes/No]

        Project: {project_name}
        Link: {github_link}
        """

        # Wait and send prompt
        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Send a message']"))
        )
        input_box.send_keys(prompt)
        input_box.send_keys(Keys.RETURN)

        # Wait for response
        time.sleep(5)  # Simulate waiting
        responses = driver.find_elements(By.XPATH, "//div[contains(@class,'message') and contains(@class,'assistant')]")
        response = responses[-1].text if responses else "No response"

        # Append results
        results.append({
            "Project Name": project_name,
            "GitHub Link": github_link,
            "Response": response,
        })

    # Save results to Excel
    output_file = "Your output file path"
    pd.DataFrame(results).to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
