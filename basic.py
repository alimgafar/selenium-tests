from selenium import webdriver
# for keyboard input, we need to import Keys
from selenium.webdriver.common.keys import Keys
# for waiting for dynamic content, we need to wait for it. Use
# implicit_wait function from WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep


driver = webdriver.Chrome()

# The site http://the-internet.herokuapp.com is a great site for testing
# selenium scripts, or any other scripts for automation.
# Good also for JavaScript scrapers.

url = ["http://the-internet.herokuapp.com/login",
       "http://the-internet.herokuapp.com/infinite_scroll", "http://the-internet.herokuapp.com/dynamic_loading/2"]


def testFormProcessing(url):
    print(url)
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="username"]').send_keys('tomsmith')
    driver.find_element_by_css_selector(
        '#password').send_keys('SuperSecretPassword!')
    driver.find_element_by_xpath('//*[@id="login"]/button').click()

    sleep(5)
    driver.find_element_by_xpath('//*[@id="content"]/div/a').click()


def testInfiniteScroll(url):
    print(url)
    driver.get(url)

    sleep(5)


def testDynamicContentWithPagination(url):
    print(url)
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="start"]/button').click()
    # wrap the implicit wait in a backoff script to poll again if
    # the page isn't ready.
    driver.implicitly_wait(15)
    text = driver.find_element_by_xpath('//*[@id="finish"]/h4').text
    print(text)


# testFormProcessing(url[0])
testDynamicContentWithPagination(url[2])
sleep(2)
driver.close()
