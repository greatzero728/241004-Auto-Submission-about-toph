import os
import time
import shutil
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv()

TOPH_USERNAME = os.getenv('TOPH_USERNAME')
TOPH_PASSWORD = os.getenv('TOPH_PASSWORD')
WAIT_TIME = int(os.getenv('WAIT_TIME'))
CHECK_RESULT_DELAY = int(os.getenv('CHECK_RESULT'))
COMMON_URL_PREFIX = "https://toph.co/p/"

# Paths to directories
SUBMISSION_DIR = './submission'
CPP_PROBLEMS_DIR = './cpp_problems'

def move_and_replace_cpp_file():
    cpp_files = [f for f in os.listdir(SUBMISSION_DIR) if f.endswith('.cpp')]
    
    if not cpp_files:
        print("No cpp files to submit. Waiting...")
        return None, None

    cpp_file = cpp_files[0]
    
    # Move and replace the cpp file in the cpp_problems directory
    src = os.path.join(SUBMISSION_DIR, cpp_file)
    dst = os.path.join(CPP_PROBLEMS_DIR, cpp_file)
    shutil.move(src, dst)
    print(f"{cpp_file} moved to cpp_problems.")

    problem_name = cpp_file.replace('.cpp', '')
    submission_url = COMMON_URL_PREFIX + problem_name
    return submission_url, dst

def login_if_needed(driver):
    try:
        login_element = driver.find_elements(By.XPATH, "//a[contains(@href, '/login')]")
        if login_element:
            print("Login required. Redirecting to login page...")
            login_element[0].click()

            username_input = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, 'handle'))
            )
            password_input = driver.find_element(By.NAME, 'password')

            username_input.send_keys(TOPH_USERNAME)
            password_input.send_keys(TOPH_PASSWORD)
            password_input.send_keys(Keys.RETURN)

            print("Logged in successfully.")
        else:
            print("Already logged in.")
    except Exception as e:
        print(f"Error during login: {e}")

def submit_cpp_file(driver, url, cpp_file_path):
    try:
        driver.get(url)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        language_dropdown = Select(WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "inpLanguageId"))
        ))

        available_languages = [option.get_attribute('innerHTML') for option in language_dropdown.options]
        if "C++23 GCC 13.2" not in available_languages:
            print("Available languages:", available_languages)
            print("There isn't 'C++23 GCC 13.2' language so, this task is invalid: ")
            return

        print("Selecting language 'C++23 GCC 13.2'...")
        driver.execute_script('document.getElementById("inpLanguageId").value = "5d828f1e9d55050001e97ee4";document.getElementById("inpLanguageId").dispatchEvent(new Event("change"));')

        cpp_file_absolute_path = os.path.abspath(cpp_file_path)
        print(f"Uploading {cpp_file_absolute_path}...")
        file_input = driver.find_element(By.NAME, "source")
        file_input.send_keys(cpp_file_absolute_path)

        print("File uploaded successfully.")
        driver.maximize_window()
        submit_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#pnlSubmit > div.panel__foot.-shade > div > button"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        print("Pressing the 'Submit' button...")
        submit_button.click()

        print("Submission made successfully.")
        check_submission_result(driver)

    except Exception as e:
        print(f"Error occurred: {e}")

def check_submission_result(driver):
    try:
        while True:
            print(f"Waiting {CHECK_RESULT_DELAY} seconds before checking the result...")
            time.sleep(CHECK_RESULT_DELAY)

            print("Fetching submission result...")
            result_row = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'syncer')]"))
            )
            problem_link = result_row.find_element(By.XPATH, ".//td[4]/a").text
            verdict = result_row.find_element(By.XPATH, ".//td[6]/span").text

            if verdict in ["Accepted", "Wrong answer", "CPU limit exceeded", "Memory limit exceeded", "Output limit exceeded", "Runtime error", "Compilation error", "Internal error"]:
                print(f"Problem: {problem_link}, Result: {verdict}")
                break
            else:
                print(f"Problem: {problem_link}, Result: Pending")
    except Exception as e:
        print(f"Error while checking result: {e}")

def main():
    driver = webdriver.Chrome()

    try:
        driver.get("https://toph.co")
        login_if_needed(driver)

        while True:
            submission_url, cpp_file_path = move_and_replace_cpp_file()

            if submission_url and cpp_file_path:
                print(f"Opening submission URL: {submission_url}")
                submit_cpp_file(driver, submission_url, cpp_file_path)

            time.sleep(WAIT_TIME)
    
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
