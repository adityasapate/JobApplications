import pandas
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, './../Requirements/')

import functions

# Global Variables
web_driver = "./../Requirements/msedgedriver"
website = 'https://www.iimjobs.com'
portal = 'IIMJOBS'
login_details_location = './../../../Backup/login_details.csv'
login_id = ''
password = ''

csv_columns = ['Job Code', 'Title', 'Hashtag', 'Description', 'Last Login', 'Posted By',
               'Position', 'Posted In', 'Location', 'Views', 'Applications', 'Recruiter Actions']
dict_data = []

iter_max = 3  # how deep do you want to go in the loop

login_placeholder_class = 'large-email'
password_placeholder_class = 'large-password'
submit_button_class = 'button-submit'

job_cluster_class = 'listingPanel'
job_row_class = 'jobRow'
save_later_class = 'saved-job'
job_title_class = 'col-lg-9new'
link_class = 'mrmob5'
job_description_class = 'job-description'
apply_button_class = 'apply_button'
job_details_class = 'mt5'
filter_button_class = 'filterlist'
workex_filter_class = 'selectBox-dropdown'
workex_chooser_class = 'selectBox-dropdown-menu'
location_chooser_class = 'divcheckboxlist'
title_class = 'jdhding'
hastag_class = 'list-inline'
click_apply_id = 'job-apply-single'
applyjobid = 'applyJob'
location_input = 'Mumbai'

output_file = './../Output/IIMJOBS'


#
# Main function to start applying for jobs
#
if __name__ == "__main__":

    # Start chrome webdriver
    driver = functions.open_browser(web_driver)

    # Retrieve login details
    print("Getting details of ID and password")
    login_details = functions.import_csv(login_details_location)
    for i in range(0, len(login_details)):
        if login_details.loc[i, 'website'] == portal:
            loginid = login_details.loc[i, 'loginid']
            password = login_details.loc[i, 'password']

    # Open website
    driver.get(website)

    # Login into the website
    print("Logging into the website")
    driver = functions.login_function(
        driver, login_placeholder_class, loginid, password_placeholder_class, password)
    functions.timeout(3)

    # Close the browser
    functions.quit_browser(driver)

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    final_output = output_file + ' iimjobs ' + dt_string + '.csv'
    functions.write_to_csv(final_output, dict_data, csv_columns)
