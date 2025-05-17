import pytest
from playwright.sync_api import sync_playwright

def go_get_page(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com/automation-practice-form")

    return page, browser



def test_good_values_validated():
    """
        Se testeaza daca dupa ce se introduc date intr-un field, borderul acestuia devine verde.
    """
    with sync_playwright() as p:

        page, browser = go_get_page(p)

        page.fill("#firstName", "Ancuta")
        page.fill("#lastName", "Vlad")
        page.fill("#userNumber", "1234567890")

        page.locator("#submit").scroll_into_view_if_needed()
        page.click("#submit")

        page.wait_for_timeout(500)
        for locator in ["#lastName", "#firstName", "#userNumber"]:
            border_color = page.locator(locator).evaluate(
                "el => getComputedStyle(el).borderColor"
            )
            assert border_color == "rgb(40, 167, 69)", f"Expected green border, got {border_color}"

        browser.close()



def test_no_mandatory_value_error():
    """"
        Se testeaza daca apare eroare semnalata prin boder rosu al unui field
        obligatoriu ce nu a fost completat inainte de a se apasa submit.
    """
    with sync_playwright() as p:
        page, browser = go_get_page(p)

        page.locator("#submit").scroll_into_view_if_needed()
        page.click("#submit")

        page.wait_for_timeout(500)

        for locator in ["#lastName", "#firstName", "#userNumber"]:
            border_color = page.locator(locator).evaluate(
                "el => getComputedStyle(el).borderColor"
            )
            assert border_color == "rgb(220, 53, 69)", f"Expected red border, got {border_color}"

        browser.close()



def test_submit_form_check_summary():
    """
    Se completeaza formularul si se verifica daca summary-ul ofera informatia corecta
    """
    with sync_playwright() as p:
        page, browser = go_get_page(p)

        page.fill("#firstName", "Ana")
        page.fill("#lastName", "Popescu")
        page.fill("#userEmail", "ana.popescu@example.com")
        page.click('label[for="gender-radio-2"]')   # F
        page.fill("#userNumber", "0712345678")

        page.locator("#submit").scroll_into_view_if_needed()
        page.click("#submit")

        page.wait_for_timeout(1000)

        def get_table_value(label):
            return page.locator(f"//td[text()='{label}']/following-sibling::td").inner_text()

        assert get_table_value("Student Name") == "Ana Popescu"
        assert get_table_value("Student Email") == "ana.popescu@example.com"
        assert get_table_value("Gender") == "Female"
        assert get_table_value("Mobile") == "0712345678"

        browser.close()

@pytest.mark.xfail(reason='email ar trebui sa fie mandatory dar nu se coloreaza rosu daca ramane necompletat')
def test_bad_email_xfail():

    with sync_playwright() as p:

        page, browser = go_get_page(p)

        page.fill("#firstName", "Ancuta")
        page.fill("#lastName", "Vlad")
        page.fill("#userNumber", "1234567890")

        page.locator("#submit").scroll_into_view_if_needed()
        page.click("#submit")

        page.wait_for_timeout(500)

        locator = "#userEmail"
        border_color = page.locator(locator).evaluate(
            "el => getComputedStyle(el).borderColor"
        )
        assert border_color == "rgb(220, 53, 69)", f"Expected red border, got {border_color}"

        browser.close()
