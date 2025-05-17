from playwright.sync_api import sync_playwright
import pytest

def test_compatibilitate_browsere():
    for browser_type in ["chromium", "firefox", "webkit"]:
        with sync_playwright() as p:

            browser = getattr(p, browser_type).launch(headless=False)
            page = browser.new_page()
            page.goto("https://fmi.unibuc.ro/")

            for option in {"planuri-de-invatamant", "admitere", "studenti", "profesori"}:
                page.click(f"a[href='/{option}/']")
                page.wait_for_timeout(1000)
                assert page.url == f"https://fmi.unibuc.ro/{option}/"
                page.go_back()
                page.wait_for_timeout(1000)
                assert page.url == "https://fmi.unibuc.ro/"

            browser.close()
