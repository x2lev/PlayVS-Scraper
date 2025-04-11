from formatter import format_team
from selenium import webdriver
from scraper import scrape_team

if __name__ == '__main__':
    team_names = [
        'Patriot Smash 1',
        'Fossil Ridge Varsity Smash Bros',
        'RMHS Lobos Varsity',
        'Kadet Smash Bros',
        'Creek Smash Red Team',
        'Gastric Doctors',
        'Regret Squad LHS Varsity A',
        'King Falcons',
        'DCHS Varsity Smash',
        'Lancer Esports',
        'FCHS Smash A',
        'Rizzlers',
        'ACHS Varsity',
        'Dayspring Eagles',
        'San Pedro Gaming',
        'Thunderhawks A',
        'DCCHS SSBU 1'
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
