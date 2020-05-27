import pandas
from selenium.webdriver.common.keys import Keys
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, './../Requirements/')
import functions

# Global Variables
web_driver = "./../Requirements/chromedriver"
website = 'https://www.iimjobs.com'
login_details_location = './../../../Backup/login_details.csv'
portal = 'IIMJOBS'
login_id = ''
password = ''

login_placeholder_class = 'large-email'
password_placeholder_class = 'large-password'
submit_button_class = 'button-submit'

job_row_class = 'jobRow'









#
# Main function to start applying for jobs
#
if __name__ == "__main__":

    # Start chrome webdriver
    driver = functions.open_browser(web_driver)

    # Retrieve login details
    login_details = functions.import_csv(login_details_location)
    for i in range (0,len(login_details)):
        if login_details.loc[i,'website'] == portal:
            loginid = login_details.loc[i,'loginid']
            password = login_details.loc[i,'password']

    # Open website
    driver.get(website)

    # Login into website
    functions.write_into_class(driver, login_placeholder_class, loginid)
    functions.write_into_class(driver, password_placeholder_class, password+Keys.ENTER)

    functions.timeout(2)

    
    # Apply for the job


    # Download the data


    # List of skills required sheet

    # Close the browser
    functions.close_browser(driver)
