# Matteo Palarchio
# matteogp.github.io

# debug bool to control tracing
debug = False

import sys, time, pprint, getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# function definitions

# login to instagram account with given credentials & navigate to account page
#   user may be prompted if they have secondary verification enabled to provide
#   their verification code
def login(driver, user, p):

    # navigate to login page & enter user credentials
    driver.get("https://www.instagram.com/accounts/login/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys(user)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(p)
    driver.find_element_by_xpath("//span/button").click()

    # brief wait to submit credentials
    WebDriverWait(driver, 2)
    attemptlogin = True

    # try login procedure, only exit if there is a sucess or displayed error message
    # attempting to catch the exceptions that can arise during login process & handle them
    while (True):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Profile")))
            if (debug): print "Sucess"
            break
        except TimeoutException:
            if (debug): print "Initial Attempt Failed"
            try:
                desc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "verificationCodeDescription")))
                print desc.text
                vercode = raw_input(">")
                driver.find_element_by_xpath("//div/input[@name='verificationCode']").clear()
                driver.find_element_by_xpath("//div/input[@name='verificationCode']").send_keys(vercode)
                driver.find_element_by_xpath("//span/button").click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
                if (debug): print "Verified"
                break
            except TimeoutException:
                if (debug): print "Error Handling"
                msg = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//form/div/p[@role="alert"]'))).text
                return msg.encode("utf-8")

    # reached if the login is successful
    driver.find_element_by_xpath("//a[text()='Profile']").click()
    return True

# scroll to bottom of a given element
def scroll_element_to_bottom(elem):
    current = 1
    prev = 0

    #repeatedly scroll down until no change happens from scrolling (reach bottom)
    while (current != prev):
        prev = current
        current = driver.execute_script('return arguments[0].scrollHeight', elem)
        if (debug): print "prev", prev, "current", current
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', elem)
        time.sleep(1.5)

# open the followers from a profile, browse all and return a list of usernames
def get_followers(driver, user):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ('//h1'))))

    driver.find_element_by_partial_link_text("follower").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span/button[text()="Following"]')))

    modal = driver.find_element_by_class_name('_gs38e')
    scroll_element_to_bottom(modal)

    find_followers = driver.find_elements(By.XPATH, "//ul/li/div/div/div/div/a")
    retlist = [e.text.encode("utf-8") for e in find_followers]
    driver.execute_script("window.history.go(-1)")
    driver.refresh()
    time.sleep(1.5)
    return retlist

# open who is followed by a profile, browse all and return a list of usernames
def get_following(driver, user):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ('//h1'))))

    driver.find_element_by_partial_link_text("following").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span/button[text()="Following"]')))

    modal = driver.find_element_by_class_name('_gs38e')
    scroll_element_to_bottom(modal)

    find_following = driver.find_elements(By.XPATH, "//ul/li/div/div/div/div/a")
    retlist = [e.text.encode("utf-8") for e in find_following]
    driver.execute_script("window.history.go(-1)")
    driver.refresh()
    time.sleep(1.5)
    return retlist

# given lists of followers and following, return a list of usernames that don't follow back
def compare_ff(followers, following):
    accounts = []
    for a in following:
        if a not in followers: accounts.append(a)
    return accounts

#logout of account from profile page
def logout (driver):
    driver.find_element_by_xpath("//button[text()='Options']").click()
    driver.find_element_by_xpath("//button[text()='Log Out']").click()

# main script

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome('executables/chromedriver')

# repeatedly attempt to login, allowing user to re-enter credentials if there is an error
while (True):
    username = raw_input("What is your instagram username? \n>")
    if (username == "q"): sys.exit()
    password = getpass.getpass("What is your instagram password? \n>")
    retval = login(driver, username, password)
    if (retval == True): break
    print retval

# get followers/following, compare & print those who don't follow back
followers = get_followers(driver, username)
following = get_following(driver, username)
outliers = compare_ff(followers, following)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(outliers)
logout(driver)
driver.close()
