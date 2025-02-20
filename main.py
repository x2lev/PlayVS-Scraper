import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

team_to_scrape = 'North Smash B'

driver = webdriver.Firefox()
action_chains = ActionChains(driver)
driver.get('https://app.playvs.com/app/standings')

driver.implicitly_wait(5)

# Login
driver.find_element(By.CSS_SELECTOR, 'button[class="onetrust-close-btn-handler ot-close-icon banner-close-button"]').click()
with open('login', 'r') as f:
    email, password = f.readlines()
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

driver.implicitly_wait(5)

# Go to Smash Standings
driver.find_element(By.XPATH, '//*[text()[contains(.,"League of Legends")]]').click()
input('hi!!!')
driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Colorado CHSAA Super Smash Bros.™ Ultimate"]').click()
driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Spring 2021"]').click()
driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Spring 2025"]').click()

driver.implicitly_wait(5)

# Find the team
if not team_to_scrape:
    team_to_scrape = input('Enter the team to scrape: ')
teams = driver.find_element(By.CSS_SELECTOR, 'div[role="rowgroup"]')
action_chains.move_to_element(teams) \
             .click(teams) \
             .key_down(Keys.PAGE_DOWN, teams) \
             .perform()

action_chains.key_down(Keys.PAGE_DOWN, teams) \
             .key_up(Keys.PAGE_DOWN, teams) \
             .key_down(Keys.PAGE_DOWN, teams) \
             .key_up(Keys.PAGE_DOWN, teams) \
             .perform()

# driver.find_element(By.XPATH, f'//p[text()="{team_to_scrape}"]').click()
input('press enter to close!')
driver.close()
