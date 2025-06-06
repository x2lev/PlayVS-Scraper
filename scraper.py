import time
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

STANDINGS_URL = 'https://app.playvs.com/app/standings'

def scrape_team(team_name, driver):
    action_chains = ActionChains(driver)
    driver.get(STANDINGS_URL)

    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, 'html') \
          .send_keys(Keys.CONTROL, Keys.SUBTRACT)

    # Login
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
    driver.implicitly_wait(5)
    with open('login', 'r', encoding='UTF-8') as f:
        email, password = f.readlines()
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.implicitly_wait(5)

    # Go to Smash Standings
    driver.find_element(By.XPATH, '//p[contains(text(),"League of Legends")]').click()
    driver.find_element(By.XPATH, '//p[contains(text(),"Super Smash Bros")]').click()

    if not driver.find_elements(By.XPATH, '//p[text()="Spring 2025"]'):
        driver.find_element(By.XPATH, '//p[contains(text(), "Spring") '\
                                        'or contains(text(), "Fall")]').click()
        driver.find_element(By.XPATH, '//p[text()="Spring 2025"]').click()
    
    if not driver.find_elements(By.XPATH, '//p[text()="Regular Season"]'):
        driver.find_element(By.XPATH, '//p[contains(text(), "Playoffs")]').click()
        driver.find_element(By.XPATH, '//p[text()="Regular Season"]').click()
    
    driver.implicitly_wait(5)

    # Find the team
    action_chains.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    while True:
        time.sleep(0.5)
        overall = driver.find_element(By.XPATH,
                                        '//p[text()="Overall"]/..//following-sibling::div/*')
        for p in overall.find_elements(By.CSS_SELECTOR, 'p'):
            if p.text == team_name:
                TEAM_P = p
                break
        else:
            TEAM_P = None
            overall.send_keys(Keys.PAGE_DOWN)
        if TEAM_P:
            try:
                TEAM_P.click()
                break
            except ElementClickInterceptedException:
                overall.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    driver.implicitly_wait(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    def scrape_matches(s):
        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
                try:
                    driver.find_element(By.XPATH, '//div[text()="Show More"]').click()
                    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
                except NoSuchElementException:
                    pass
                break
            except ElementClickInterceptedException:
                pass
        match_history = driver.find_element(By.CSS_SELECTOR,
                                            'div[data-testid="TeamOverview_MatchHistory"]')
        matches = match_history.find_elements(By.CSS_SELECTOR, 'li')
        for match in matches:
            try:
                match.find_element(By.CSS_SELECTOR, 'img').click()
                data.append([])
                time.sleep(5)
                driver.implicitly_wait(5)

                driver.switch_to.window(driver.window_handles[1])
                banner = driver.find_element(By.CSS_SELECTOR,
                                            'div[data-testid="NxEsportBanner__TextContainer"]')
                is_home = banner.find_element(By.CSS_SELECTOR, 'span').text == team_name

                scoreboard = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="scoreboard-rows"]')
                for series in scoreboard.find_elements(By.XPATH, '*'):
                    data[-1].append({})
                    try:
                        header, body = series.find_elements(By.XPATH, '*')
                        names = [p.text for p in header.find_elements(By.CSS_SELECTOR, 'p') if p.text == p.get_attribute('data-cy')]
                        data[-1][-1]['name'] = names[0 if is_home else 1]
                        data[-1][-1]['games'] = []
                        for game in body.find_elements(By.XPATH, '*/*'):
                            data[-1][-1]['games'].append({})
                            data[-1][-1]['games'][-1]['season'] = s
                            stage = game.find_element(By.XPATH, '//p[contains(text(), "Game")]'
                                                                '/following-sibling::p').text
                            data[-1][-1]['games'][-1]['stage'] = stage
                            chars = [c.get_attribute('alt') 
                                    for c in game.find_elements(By.CSS_SELECTOR, 'img')]
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
                            print(data[-1][-1]['name'], data[-1][-1]['games'][-1])
                    except ValueError:
                        header = series.find_elements(By.XPATH, '*')[0]
                        texts = [p.text for p in header.find_elements(By.CSS_SELECTOR, 'p') if p.text]
                        names = [t for t in texts if all(x.isalpha() or x in " -'" for x in t)]
                        data[-1][-1]['name'] = names[0 if is_home else 1]
                        data[-1][-1]['games'] = []
                driver.switch_to.window(driver.window_handles[0])
            except NoSuchElementException:
                pass

        windows = len(driver.window_handles)
        for _ in range(windows-1):
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

    data = [team_name]
    driver.find_element(By.XPATH, '//p[text()="Spring 2025"]').click()
    seasons = [s.find_element(By.CSS_SELECTOR, 'p').text for s in driver.find_elements(By.XPATH,
                            '//li[contains(@data-cy, "Spring") or contains(@data-cy, "Fall")]')][::-1]
    action_chains.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
    scrape_matches('Spring 2025')
    driver.find_element(By.XPATH, '//p[text()="Playoffs"]').click()
    driver.find_element(By.XPATH, '//p[text()="Regular Season"]').click()
    driver.implicitly_wait(5)
    scrape_matches('Spring 2025')
    for i in range(1, len(seasons)):
        if seasons[i] == 'Fall 2024': #int(seasons[i].split(' ')[1]) > 2023 or seasons[i] == 'Fall 2023':
            driver.find_element(By.XPATH, f'//p[text()="{seasons[i-1]}"]').click()
            driver.find_element(By.XPATH, f'//p[text()="{seasons[i]}"]').click()
            driver.implicitly_wait(5)
            scrape_matches(seasons[i])
            try:
                driver.find_element(By.XPATH, '//p[text()="Playoffs - Semi Finals / Finals"]').click()
                driver.find_element(By.XPATH, '//p[text()="Playoffs"]').click()
                driver.implicitly_wait(5)
                scrape_matches(seasons[i])
            except NoSuchElementException:
                pass
            driver.find_element(By.XPATH, '//p[text()="Playoffs"]').click()
            driver.find_element(By.XPATH, '//p[text()="Regular Season"]').click()
            driver.implicitly_wait(5)
            scrape_matches(seasons[i])

    with open(f'match_data/{team_name}.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(data, indent=4))
