from playwright.sync_api import Playwright, sync_playwright
import pandas as pd
import openpyxl

data = []

def parse(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    page = context.new_page()
    page.set_default_timeout(50000)
    page.goto("https://www.python.org/downloads/")
    page.wait_for_selector(".row download-list-widget")
    table = page.query_selector(".list-row-container menu")
    ol_list = table.query_selector("ol")
    li_list = ol_list.query_selector_all("li")
    for li in li_list:
        data.append({
            'release-version': li.query_selector(".release-number").query_selector("a").get_attribute("href"),
            'release-date': li.query_selector(".release-date").text_content(),
            'release-download': li.query_selector(".release-download").query_selector("a").get_attribute("href"),
            'Release Notes': li.query_selector(".release-enhancements").query_selector("a").get_attribute("href"),
        })
    return data


with sync_playwright() as playwright:
    parse(playwright)

df = pd.DataFrame(data)

df.to_excel('releases.xlsx', index=False)