from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import json
import time

def get_expenses_by_year(year):
    chrome_opt = Options()
    chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--no-sandbox')
    chrome_opt.add_argument('--disable-dev-sh--usage')

    # Set up the Chrome WebDriver object
    driver = webdriver.Remote("https://selenium-standalone-test.onrender.com/wd/hub", options=chrome_opt)

    # Navigate to the website with the button you want to click
    driver.get("https://transparencia.tce.ce.gov.br/portal/paginas/execucao-Orcamentaria-da-Despesa.xhtml")

    # Select correct iframe
    # WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'blockrandom')))

    # Select anual based search
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form:tipo:1"]'))
    )
    button.click()

    # Select year
    ano = Select(WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'form:ano'))
    ))
    ano.select_by_value(year)

    # wait to click
    time.sleep(1)

    # Click search
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'form:j_idt68'))
    )
    button.click()

    # time.sleep(2)

    # Click see all
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'form:btnExpanded'))
    )
    button.click()

    table = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "arvore"))
    )

    titles = []
    values = []
    if table:
        table_head = table.find_elements(By.TAG_NAME, "th")
        for th in table_head:
            titles.append(th.text)
        table_body = table.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            obj = {}
            for idx, td in enumerate(tds):
                obj[titles[idx]] = td.text
            values.append(obj)
        return values
    else:
        return json.dumps({"error": "Table not found"})
    

    # time.sleep(10)

    # Close the WebDriver
    driver.quit()
