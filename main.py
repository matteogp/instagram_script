import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
# Create a new instance of the Chrome driver
driver = webdriver.Chrome('/Users/mgp/Documents/Dev/executables/chromedriver')

# login to instagram account with given credentials & navigate to account page
#   user may be prompted if they have secondary verification enabled to provide
#   their verification code
def login(driver, user, p):

    # navigate to login page & enter user credentials
    driver.get("https://www.instagram.com/accounts/login/")
    driver.find_element_by_xpath("//div/input[@name='username']").send_keys(user)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(p)
    driver.find_element_by_xpath("//span/button").click()

    # brief wait to submit credentials
    WebDriverWait(driver, 2)
    attemptlogin = True

    # try login procedure, only exit if there is a sucess or displayed error message
    while (True):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "See All")))
            break
        except TimeoutException:
            try:
                desc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "verificationCodeDescription")))
                print desc.text
                vercode = input(">")
                driver.find_element_by_xpath("//div/input[@name='verificationCode']").clear()
                driver.find_element_by_xpath("//div/input[@name='verificationCode']").send_keys(vercode)
                driver.find_element_by_xpath("//span/button").click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
                break
            except TimeoutException:
                try:
                    msg = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "Error")))
                    return msg
                except TimeoutException: continue

    driver.find_element_by_xpath("//a[text()='Profile']").click()
    return True

def get_followers(driver, user):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ("//h1[@title='{0}']").format(user))))
    driver.find_element_by_partial_link_text("follower").click()
    wait = WebDriverWait(driver, 2)
    find_followers = driver.find_elements_by_xpath("//div[@style='position: relative; z-index: 1;']//ul/li/div/div/div/div/a")
    print "yay"
    return [e.text for e in find_followers]

def get_following(driver, user):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ("//h1[@title='{0}']").format(user))))
    driver.find_element_by_partial_link_text("following").click()




# repeatedly attempt to login, allowing user to re-enter credentials if there is an error
'''
while (True):
    username = raw_input("What is your instagram username? \n>")
    if (username == "q"): sys.exit()
    password = raw_input("What is your instagram password? \n>")
    retval = login(driver, username, password)
    if (retval == True): break
    print retval
'''
if (False):
    username = "matteogp_test"
    password = "test123"
else:
    username = "matteo_gp"
    password = "BSYZfpt78"

login(driver, username, password)
followers = get_followers(driver, username)
print followers
'''
file1 = open("d1.txt")
file2 = open("d2.txt")

followers = file1.readlines()
following = file2.readlines()

unfollow = []

def strip_list (lst):
  alt = 2
  newlst = []
  for f in lst:
    if (alt==3):
      f.strip()
      alt = 0
      newlst.append(f)
    else:
      alt+=1
  return newlst

#followers = strip_list(followers)
print("--")
following = strip_list(following)

for account in following:
  if account not in followers:
    unfollow.append(account)
    print(account + "\n")
'''
