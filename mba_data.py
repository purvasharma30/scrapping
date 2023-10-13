from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# URL to scrape
URL = 'https://www.shiksha.com/studyabroad/masters-of-law-in-abroad-cl1245-11'

# Initialize Chrome options and WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
driver = webdriver.Chrome(options=chrome_options)

# Open the URL
driver.get(URL)

# Initialize lists to store scraped data
college_names = []
locations = []
fees_list = []
exams_list = []
workexp_list = []
scholarships_list = []
intake_sessions_list = []
links = []

# Scroll to the bottom of the page to load more colleges
scroll_height = 0
while True:
    # Scroll down a little bit
    driver.execute_script("window.scrollTo(0, {});".format(scroll_height))

    # Wait for a short delay (adjust as needed)
    time.sleep(1)

    # Increase the scroll height
    scroll_height += 300  # Adjust the scroll amount as needed

    # Check if we have reached the bottom of the page
    if scroll_height >= driver.execute_script("return document.body.scrollHeight;"):
        break

# Find the elements containing college details
college_elements = driver.find_elements(By.XPATH, '//div[contains(@id, "tuple_")]')

# Loop through each college element
for college_element in college_elements:
    try:
        # Extract College Name
        college_name_element = college_element.find_element(By.XPATH, './/div[1]/div/div/div[2]/div[1]/a/h3')
        college_name = college_name_element.text

        # Extract Location
        location_element = college_element.find_element(By.XPATH, './/div[1]/div/div/div[2]/div[2]/span[1]/span')
        location = location_element.text

        # Extract Fees
        fees_element = college_element.find_element(By.XPATH, './/div[2]/div[1]/div[2]/div')
        fees = fees_element.text

        # Extract Exams
        exams_element = college_element.find_element(By.XPATH, './/div[2]/div[1]/div[3]/div/ul')
        exams = exams_element.text

        # Extract WorkExp
        workexp_element = college_element.find_element(By.XPATH, './/div[2]/div[1]/div[4]/div')
        workexp = workexp_element.text

        # Extract Scholarship
        scholarship_element = college_element.find_element(By.XPATH, './/div[2]/div[1]/div[5]/div')
        scholarships = scholarship_element.text

        # Extract Intake Session
        intake_session_element = college_element.find_element(By.XPATH, './/div[2]/div[1]/div[6]/div')
        intake_sessions = intake_session_element.text

        # Extract the Link
        link_element = college_element.find_element(By.XPATH, './/div[1]/div/div/div[2]/div[1]/a')
        link = link_element.get_attribute('href')

        # Append data to lists
        college_names.append(college_name)
        locations.append(location)
        fees_list.append(fees)
        exams_list.append(exams)
        workexp_list.append(workexp)
        scholarships_list.append(scholarships)
        intake_sessions_list.append(intake_sessions)
        links.append(link)

    except Exception as e:
        print(f"An error occurred while scraping college data: {e}")

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'College name': college_names,
    'Location': locations,
    'Fees': fees_list,
    'Exams': exams_list,
    'WorkExp': workexp_list,
    'Scholarship': scholarships_list,
    'Intake session': intake_sessions_list,
    'Link': links
})

# Save the final scraped data to a new Excel file
data.to_excel('scraped_data_final.xlsx', index=False)

# Close the WebDriver
driver.quit()
