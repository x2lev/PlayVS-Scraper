from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TEAM_TO_SCRAPE = 'Kadet Smash Bros'
if not TEAM_TO_SCRAPE:
    TEAM_TO_SCRAPE = input('Enter the team to scrape: ')

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
teams = driver.find_element(By.XPATH, '//p[text()="Overall"]/..//following-sibling::div/*')
#with open('output.html', 'w', encoding='UTF-8') as f:
#    f.write(teams.get_attribute('outerHTML'))
while True:
    teams.send_keys(Keys.PAGE_DOWN)
    try:
        team = driver.find_element(By.XPATH, f'//p[text()="{TEAM_TO_SCRAPE}"]')
        break
    except NoSuchElementException:
        pass

with open('output.html', 'w', encoding='UTF-8') as f:
    f.write(team.get_attribute('outerHTML'))

team.click()
input('press enter to close!')
driver.close()
