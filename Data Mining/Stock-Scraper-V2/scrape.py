from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


driver = webdriver.Chrome()

pageFrom = 1
pageTo = 75
pageCurrent = pageFrom

while pageCurrent <= pageTo:

    driver.get("https://www.capitoltrades.com/trades" + "?page=" + str(pageCurrent))
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tr.q-tr")))
    trade_elements = driver.find_elements(By.CSS_SELECTOR, "tr.q-tr")

    with open('data/Scrape 2/trades_' + str(pageCurrent) + '.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(["Politician Name", "Party", "Chamber", "State", "Issuer Name", "Ticker", "Publication Date",
        #                  "Transaction Date", "Reporting Gap", "Owner", "Transaction Type", "Value Range", "Price",
        #                  "Transaction ID"])

        for trade in trade_elements:
            # Check if the transaction ID exists and is not empty
            transaction_link = trade.find_elements(By.CSS_SELECTOR, ".entity-link.entity-transaction")
            if transaction_link and transaction_link[0].get_attribute('href'):
                # Your existing data extraction logic goes here
                politician_name = trade.find_element(By.CSS_SELECTOR, ".politician-name a").text
                party = trade.find_element(By.CSS_SELECTOR, ".party--democrat, .party--republican, .party--other").text
                chamber = trade.find_element(By.CSS_SELECTOR, ".chamber").text
                state = trade.find_element(By.CSS_SELECTOR, ".us-state-compact").text
                issuer_name = trade.find_element(By.CSS_SELECTOR, ".issuer-name a").text
                ticker = trade.find_element(By.CSS_SELECTOR, ".issuer-ticker").text
                publication_date = trade.find_element(By.CSS_SELECTOR, ".cell--pub-date .q-value").text
                transaction_year = trade.find_element(By.CSS_SELECTOR, ".cell--tx-date .q-label").text
                transaction_date = trade.find_element(By.CSS_SELECTOR, ".cell--tx-date .q-value").text
                reporting_gap = trade.find_element(By.CSS_SELECTOR, ".cell--reporting-gap .q-value").text
                owner = trade.find_element(By.CSS_SELECTOR, ".owner-with-icon span.q-label").text
                transaction_type = trade.find_element(By.CSS_SELECTOR, ".tx-type").text
                value_range = trade.find_element(By.CSS_SELECTOR, ".trade-size .q-label").text
                price = trade.find_element(By.CSS_SELECTOR, ".cell--trade-price").text if trade.find_element(
                    By.CSS_SELECTOR,
                    ".cell--trade-price").text != "N/A" else "N/A"
                transaction_id = \
                    trade.find_element(By.CSS_SELECTOR, ".entity-link.entity-transaction").get_attribute("href").split("/")[
                        -1]
                full_transaction_date = f"{transaction_date} {transaction_year}"

                # Write the extracted data to the CSV
                writer.writerow(
                    [politician_name, party, chamber, state, issuer_name, ticker, publication_date, full_transaction_date,
                     reporting_gap, owner, transaction_type, value_range, price, transaction_id])

    print('Scraped page', pageCurrent)
    pageCurrent += 1


driver.quit()