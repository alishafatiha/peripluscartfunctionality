from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def open_cart(driver, wait):
    driver.get("https://www.periplus.com/checkout/cart")
    wait_for_page(driver)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)


def verify_cart_page(driver):
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    return "remove" in body_text or "save for later" in body_text or "shopping cart" in body_text


def get_first_cart_item_name(driver):
    possible_locators = [
        (By.TAG_NAME, "h2"),
        (By.CSS_SELECTOR, "h2"),
        (By.CSS_SELECTOR, "div[class*='product'] h2"),
        (By.CSS_SELECTOR, "div[class*='cart'] h2"),
    ]

    for by, locator in possible_locators:
        elements = driver.find_elements(by, locator)
        for el in elements:
            text = el.text.strip()
            if text:
                return text

    return None


def remove_product_from_cart(driver, wait):
    remove_locators = [
        (By.CSS_SELECTOR, "a.btn.btn-cart-remove"),
        (By.CSS_SELECTOR, "a.btn-cart-remove"),
        (By.XPATH, "//a[contains(@class,'btn-cart-remove')]"),
        (By.XPATH, "//a[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'REMOVE')]"),
    ]

    last_error = None

    for by, locator in remove_locators:
        try:
            remove_button = wait.until(EC.presence_of_element_located((by, locator)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remove_button)
            time.sleep(1)

            try:
                wait.until(EC.element_to_be_clickable((by, locator)))
                remove_button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", remove_button)

            time.sleep(3)
            return True

        except Exception as e:
            last_error = e
            continue

    print("Remove click failed:", repr(last_error))
    return False


def verify_cart_item_removed(driver, selected_name):
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    if selected_name:
        return selected_name.lower() not in body_text

    return "remove" not in body_text


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

        open_cart(driver, wait)

        if verify_cart_page(driver):
            print("Cart page opened successfully")
        else:
            print("Cart page could not be verified")

        selected_name = get_first_cart_item_name(driver)
        print("Cart item:", selected_name)

        removed = remove_product_from_cart(driver, wait)

        if removed:
            print("Remove button clicked")
        else:
            print("Remove button was not clicked")

        wait_for_page(driver)
        time.sleep(2)

        if verify_cart_item_removed(driver, selected_name):
            print("Product removed successfully")
        else:
            print("Product removal could not be verified")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()