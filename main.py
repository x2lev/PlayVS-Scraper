from scraper import scrape_team
from formatter import format_team
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    team_names = [
        'Patriot Smash 1',
        'Valor A Team',
        'ACHS Varsity',
        'Creek Smash Red Team',
        'Regret Squad LHS Varsity A',
        'San Pedro Gaming',
        'North Smash A',
        'RMHS Lobos Varsity',
        'Kadet Smash Bros',
        'Rizzlers',
        'Thunderhawks A',
        'Smash Team Varsity',
        'PH ISH',
        'Royal',
        'Lancer Esports',
        'Filibuster LHS Varsity B'
    ]
    for tn in team_names:
        print(tn)
        scraped = False
        formatted = False
        while not scraped or not formatted:
            if not scraped:
                driver = webdriver.Firefox()
                try:
                    scrape_team(tn, driver)
                    scraped = True
                except Exception as e:
                    print(e)
                driver.close()
            if not formatted:
                try:
                    format_team(tn)
                    formatted = True
                except Exception as e:
                    print(e)