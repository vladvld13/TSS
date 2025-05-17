from playwright.sync_api import sync_playwright
import pytest

def go_get_page(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://fmi.unibuc.ro/")

    return page, browser


def test_navigate_between_pages():

    with sync_playwright() as p:
        page, browser = go_get_page(p)
        for option in {"planuri-de-invatamant", "admitere", "studenti", "profesori"}:
            page.click(f"a[href='/{option}/']")
            page.wait_for_timeout(1000)
            assert page.url == f"https://fmi.unibuc.ro/{option}/"
            page.go_back()
            page.wait_for_timeout(1000)
            assert page.url == "https://fmi.unibuc.ro/"

        browser.close()
