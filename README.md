How to get this project up and scraping:
1. Enter login details into a file named "login" at the root of the project directory (PlayVS-Scraper/login).
The first line should be the email and the second line should be the password.
\
2. Set up a python venv at the root of the project directory (PlayVS-Scraper/venv) and install the latest selenium package (pip install selenium).
\
3. Open main.py and edit team_names list to include all the teams you want to scrape. Make sure each name is entered exactly as it is in the standings.
\
4. Run main.py and leave your computer while the program is scraping.
\
5. In the end you can find the teams you scraped as a json file of all their matches in math_data/ and a json file containing player data in team_data/. A human-readable version of the latter will be made in the formatted_data/ folder.
\\
If you don't want to go through the trouble of scraping the teams yourself, some of them have already been scraped and you can find their human-readable files in the aformetioned formatted_data/ folder. 
