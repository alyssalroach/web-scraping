import sys
import pandas
import pandera

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape(filter):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        page.goto('https://www.scrapethissite.com/pages/forms/')

        page.fill("input.form-control", filter)
        page.click("input.btn")

        html = page.inner_html("table.table")

        # get specific value we want with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        
        data_frame = pandas.DataFrame(columns=["team_name", "year", "wins"])

        for row in soup.find_all('tr'):
            columns = row.find_all('td')

            if columns != []:
                team_name = columns[0].text.strip()
                year = columns[1].text.strip()
                wins = columns[2].text.strip()
                
                data_frame = data_frame.append({"team_name": team_name, "year": year, "wins": wins}, ignore_index=True)
    
        data_frame["year"] = data_frame["year"].astype(int)
        data_frame["wins"] = data_frame["wins"].astype(int)

        # data validation with pandera
        schema = pandera.DataFrameSchema({
            "team_name": pandera.Column(str, checks=pandera.Check(lambda s: s.str.contains(filter))),
            "year": pandera.Column(int),
            "wins": pandera.Column(int)
        })

        schema.validate(data_frame, lazy=True)

        return(data_frame)

def main():
    if len(sys.argv) != 3:
        print("wrong number of arguments given")
    
    team = sys.argv[1]

    scraped_data = scrape(team)
    average = scraped_data["wins"].mean()

    print(f"The average wins per season for the {team} is {average}")

if __name__=="__main__":
    main()

