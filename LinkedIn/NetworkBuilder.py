import pandas
# some_file.py
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, './../Requirements/')
import functions

# Global Variables
web_driver = "./../Requirements/chromedriver"
website = 'https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in'
login_details_location = './../../../Backup/login_details.csv'
portal = 'LinkedIn'
login_id = ''
password = ''

login_placeholder_class = 'username'
password_placeholder_class = 'password'


element_class = 'discover-entity-type-card'
partial_text = 'Connect'
connect_button_class = 'artdeco-button--secondary'


#
# makes the application for the portal
#
def connect(driver):
    return ""


#
# Main function to start applying for jobs
#
if __name__ == "__main__":

    # Start chrome webdriver
    driver = functions.open_browser(web_driver)

    # Retrieve login details
    # print("Getting details of ID and password")
    login_details = functions.import_csv(login_details_location)
    for i in range (0,len(login_details)):
        if login_details.loc[i,'website'] == portal:
            loginid = login_details.loc[i,'loginid']
            password = login_details.loc[i,'password']

    # Open website
    driver.get(website)

    # Login into the website
    print("Logging into the website")
    driver = functions.login_function(driver, login_placeholder_class, loginid, password_placeholder_class, password)
    functions.timeout(15)

    print('Finding elements to connect')
    elements = functions.find_classes(driver, element_class)
    iter = 0
    for element in elements:
        try:
            connect_button = functions.find_class(element, connect_button_class)
            print (connect_button.text)
            if(connect_button.text == 'Connect'):
                connect_button.click()
                iter = iter + 1
                functions.timeout(1.5)
            if(iter >= 100):
                break


        except:
            continue



    # Close the browser
    functions.quit_browser(driver)
