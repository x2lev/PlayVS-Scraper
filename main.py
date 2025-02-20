import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TEAM_NAME = 'Kadet Smash Bros'
if not TEAM_NAME:
    TEAM_NAME = input('Enter the team name: ')

driver = webdriver.Firefox()
action_chains = ActionChains(driver)
driver.get('https://app.playvs.com/app/standings')

driver.implicitly_wait(5)

# Login
driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
with open('login', 'r', encoding='UTF-8') as f:
    email, password = f.readlines()
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

driver.implicitly_wait(5)

# Go to Smash Standings
driver.find_element(By.XPATH, '//p[contains(text(),"League of Legends")]').click()
driver.find_element(By.XPATH, '//p[contains(text(),"Super Smash Bros")]').click()
driver.find_element(By.XPATH, '//p[contains(text(), "Spring") or contains(text(), "Fall")]').click()
driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Spring 2025"]').click()

driver.implicitly_wait(5)

# Find the team
action_chains.send_keys(Keys.PAGE_DOWN).perform()
teams = driver.find_element(By.XPATH, '//p[text()="Overall"]/..//following-sibling::div/*')
while not (team := driver.find_elements(By.XPATH, f'//p[text()="{TEAM_NAME}"]')):
    teams.send_keys(Keys.PAGE_DOWN)
time.sleep(.5)
teams.send_keys(Keys.PAGE_DOWN)
team[0].click()

time.sleep(1)
driver.implicitly_wait(5)

# Find their matches
match_history = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="TeamOverview_MatchHistory"]')
matches = match_history.find_elements(By.CLASS_NAME, 'li')
print(matches)

input('press enter to close!')
driver.close()
