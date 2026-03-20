from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time


def wait_for_page(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def open_login_page(driver, wait):
    driver.get("https://www.periplus.com/account/Login")
    wait_for_page(driver)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


def negative_login_test(driver, wait):
    email = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "input[type='email'], input[id*='Email'], input[name*='email'], input[name*='Email']"
    )))
    password = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "input[type='password'], input[id*='Password'], input[name*='password'], input[name*='Password']"
    )))

    email.clear()
    email.send_keys("alisha.d@ifullah.com")

    password.clear()
    password.send_keys("alisha12")
    password.send_keys(Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("URL setelah submit dummy:", driver.current_url)
    print("Page title:", driver.title)
    print(driver.find_element(By.TAG_NAME, "body").text[:500])


def search_book(driver, wait, keyword):
    driver.get("https://www.periplus.com/")
    wait_for_page(driver)

    search_box = wait.until(
        EC.visibility_of_element_located((By.ID, "filter_name_desktop"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_box)
    time.sleep(1)

    search_box.clear()
    search_box.send_keys(keyword)
    print("Search value:", search_box.get_attribute("value"))

    search_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btnn[type='submit']"))
    )
    driver.execute_script("arguments[0].click();", search_button)

    wait_for_page(driver)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)


def get_product_links(driver):
    anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
    links = []
    seen = set()

    for a in anchors:
        href = a.get_attribute("href")
        if href and href not in seen:
            seen.add(href)
            links.append(href)

    return links


def product_is_available(driver):
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    unavailable_markers = [
        "currently unavailable",
        "out of stock",
        "unavailable"
    ]
    return not any(marker in body_text for marker in unavailable_markers)


def get_product_name(driver, wait):
    try:
        return wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except TimeoutException:
        return "Unknown Product"


def add_current_product_to_cart(driver, wait):
    add_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ADD TO CART')]"
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", add_btn)
    time.sleep(3)


def open_cart(driver):
    driver.get("https://www.periplus.com/Cart")
    wait_for_page(driver)
    time.sleep(2)


def verify_product_in_cart(driver, selected_name):
    cart_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    return selected_name.lower() in cart_text.lower()


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 15)

    try:
        open_login_page(driver, wait)

        negative_login_test(driver, wait)

        keyword = "great gatsby"
        search_book(driver, wait, keyword)

        product_links = get_product_links(driver)
        print(f"Found {len(product_links)} product links")

        if not product_links:
            raise Exception("Product is not found")

        selected_name = None
        added = False

        for href in product_links:
            try:
                print("Opening:", href)
                driver.get(href)
                wait_for_page(driver)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(2)

                if not product_is_available(driver):
                    print("Skip unavailable product")
                    continue

                selected_name = get_product_name(driver, wait)
                print("Selected product:", selected_name)

                # 6) add to cart
                add_current_product_to_cart(driver, wait)
                print("Add to cart clicked")

                added = True
                break

            except Exception as e:
                print("Skip product because of error:", repr(e))
                continue

        if not added:
            raise Exception("Product is not available")

        open_cart(driver)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()