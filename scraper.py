import time
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

TEAM_URL = ''#'https://app.playvs.com/app/team/76862a5c-caec-48a8-ae2d-7793d54bf037'
STANDINGS_URL = 'https://app.playvs.com/app/standings'

TEAM_NAME = 'Kadet Smash Bros'
if not TEAM_NAME:
    TEAM_NAME = input('Enter the team name: ')

driver = webdriver.Firefox()
action_chains = ActionChains(driver)
driver.get(TEAM_URL if TEAM_URL else STANDINGS_URL)

driver.implicitly_wait(5)

# Login
driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
with open('login', 'r', encoding='UTF-8') as f:
    email, password = f.readlines()
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

driver.implicitly_wait(5)

if not TEAM_URL:
    # Go to Smash Standings
    driver.find_element(By.XPATH, '//p[contains(text(),"League of Legends")]').click()
    driver.find_element(By.XPATH, '//p[contains(text(),"Super Smash Bros")]').click()
    driver.find_element(By.XPATH, '//p[contains(text(), "Spring") or contains(text(), "Fall")]').click()
    driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Spring 2025"]').click()

    driver.implicitly_wait(5)

    # Find the team
    action_chains.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    team = []
    while True:
        teams = driver.find_element(By.XPATH, '//p[text()="Overall"]/..//following-sibling::div/*')
        try:
            team = teams.find_element(By.XPATH, f'//p[text()="{TEAM_NAME}"]')
            try:
                time.sleep(0.5)
                team.click()
                break
            except ElementClickInterceptedException:
                teams.send_keys(Keys.ARROW_DOWN)
        except NoSuchElementException:
            teams.send_keys(Keys.PAGE_DOWN)

    driver.implicitly_wait(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Find their matches
match_history = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="TeamOverview_MatchHistory"]')
matches = match_history.find_elements(By.CSS_SELECTOR, 'li')

# Scrape each match
data = [TEAM_NAME]
for match in matches:
    data.append([])
    match.find_element(By.CSS_SELECTOR, 'img').click()

    time.sleep(4)
    driver.implicitly_wait(5)
    
    driver.switch_to.window(driver.window_handles[1])
    banner = driver.find_element(By.CSS_SELECTOR,
                                 'div[data-testid="NxEsportBanner__TextContainer"]')
    is_home = banner.find_element(By.CSS_SELECTOR, 'span').text == TEAM_NAME

    scoreboard = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="scoreboard-rows"]')
    for position, series in enumerate(scoreboard.find_elements(By.XPATH, '*')):
        data[-1].append({})
        try:
            header, body = series.find_elements(By.XPATH, '*')
            texts = [p.text for p in header.find_elements(By.CSS_SELECTOR, 'p') if p.text]
            names = [t for t in texts if all(x.isalpha() or x.isspace() for x in t)]
            data[-1][-1]['name'] = names[0 if is_home else 1]
            data[-1][-1]['games'] = []
            for game in body.find_elements(By.XPATH, '*/*'):
                data[-1][-1]['games'].append({})
                stage = game.find_element(By.XPATH, '//p[contains(text(), "Game")]'
                                                    '/following-sibling::p').text
                data[-1][-1]['games'][-1]['stage'] = stage
                chars = [c.get_attribute('alt') for c in game.find_elements(By.CSS_SELECTOR, 'img')]
                home_won = game.find_element(By.CSS_SELECTOR,
                                            'div[data-cy="leftTriangle"]').is_displayed()
                if is_home:
                    data[-1][-1]['games'][-1]['char'] = chars[0]
                    data[-1][-1]['games'][-1]['opp'] = chars[1]
                    data[-1][-1]['games'][-1]['result'] = 'win' if home_won else 'loss'
                else:
                    data[-1][-1]['games'][-1]['char'] = chars[1]
                    data[-1][-1]['games'][-1]['opp'] = chars[0]
                    data[-1][-1]['games'][-1]['result'] = 'win' if not home_won else 'loss'
        except ValueError:
            header = series.find_elements(By.XPATH, '*')[0]
            texts = [p.text for p in header.find_elements(By.CSS_SELECTOR, 'p') if p.text]
            names = [t for t in texts if all(x.isalpha() or x.isspace() for x in t)]
            data[-1][-1]['name'] = names[0 if is_home else 1]
            data[-1][-1]['games'] = []
    driver.switch_to.window(driver.window_handles[0])

windows = len(driver.window_handles)
for i in range(windows):
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

with open('data.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(data, indent=4))
