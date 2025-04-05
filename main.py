from formatter import format_team
from selenium import webdriver
from scraper import scrape_team

if __name__ == '__main__':
    team_names = [
        #'BHS Team 1',
        #'Pikmen 5',
        #'DSISD B',
        'Smashing Phoenix',
        'FCHS Smash B'
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
