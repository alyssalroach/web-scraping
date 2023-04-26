# playwright can be used synchronously or async, in this demo project I will be using it sync
# this is based off of the demo from https://www.youtube.com/watch?v=H2-5ecFwHHQ

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# using a context manager - closes browser when code is finished. 
with sync_playwright() as p:
    # runs headless by default 
    # slow_mo is to slow the process down so we can better see what is happening.
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()

    page.goto('https://demo.opencart.com/admin/')

    # login
    page.fill("input#input-username", "demo")
    page.fill("input#input-password", "demo")
    page.click("button[type=submit]")

    # wait for the dashboard to load
    # can also use page.is_visible
    page.wait_for_selector("div#navigation")

    # close the security notification that arises
    page.click("button.btn-close")

    # pull html data
    html = page.inner_html("#content")

    # get specific value we want with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    total_orders = soup.find("h2", {"class": "float-end"}).text
    print(f'total orders = {total_orders}')
