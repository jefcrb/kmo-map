import re
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


print(ChromeDriverManager().install())

def extract_emails_from_text(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_regex, text)

def extract_urls_from_page(driver):
    links = driver.find_elements(By.TAG_NAME, 'a')
    urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]
    return urls

def crawl(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        email_results = {}

        driver.get(url)
        time.sleep(2)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        page_source = driver.page_source
        main_page_emails = extract_emails_from_text(page_source)
        email_results[url] = main_page_emails

        urls = extract_urls_from_page(driver)

        for contact_url in urls:
            if 'contact' in contact_url.lower():
                print(f"Navigating to contact page: {contact_url}")
                driver.get(contact_url)
                time.sleep(2)
                contact_page_source = driver.page_source
                contact_page_emails = extract_emails_from_text(contact_page_source)
                email_results[contact_url] = contact_page_emails

        return email_results

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a webpage to extract emails.")
    parser.add_argument("url", type=str, help="The URL of the website to crawl")
    args = parser.parse_args()

    print(f"Beginnen met scan voor: {args.url}")

    emails_found = crawl(args.url)

    if emails_found:
        print("\nGevonden emails per URL:")
        for url, emails in emails_found.items():
            if emails:
                print(f"{url}:")
                for email in emails:
                    print(f"  - {email}")
            else:
                print(f"{url}: Geen emails gevonden")
    else:
        print("Geen emails gevonden")
