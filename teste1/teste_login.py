from playwright.sync_api import sync_playwright, expect


def test_good_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://practicetestautomation.com/practice-test-login/")

        page.fill("input#username", "student")
        page.fill("input#password", "Password123")

        page.locator("#submit").click()

        expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")

        browser.close()


def test_bad_password_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://practicetestautomation.com/practice-test-login/")

        page.fill("input#username", "student")
        page.fill("input#password", "Password1234")

        page.locator("#submit").click()

        expect(page.locator('#error')).to_be_visible()
        expect(page.locator('#error')).to_have_text("Your password is invalid!")

        browser.close()


def test_bad_username_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://practicetestautomation.com/practice-test-login/")

        page.fill("input#username", "student1")
        page.fill("input#password", "Password123")

        page.locator("#submit").click()

        expect(page.locator('#error')).to_be_visible()
        expect(page.locator('#error')).to_have_text("Your username is invalid!")

        browser.close()

