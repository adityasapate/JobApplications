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
website = 'https://www.iimjobs.com'
login_details_location = './../../../Backup/login_details.csv'
portal = 'IIMJOBS'
login_id = ''
password = ''

csv_columns =['Job Code', 'Title', 'Hashtag', 'Description', 'Last Login', 'Posted By', 'Position', 'Posted In', 'Location', 'Views', 'Applications', 'Recruiter Actions']
dict_data = []

iter_max = 2 #how deep do you want to go in the loop

login_placeholder_class = 'large-email'
password_placeholder_class = 'large-password'
submit_button_class = 'button-submit'

job_cluster_class = 'listingPanel'
job_row_class = 'jobRow'
save_later_class = 'saved-job'
job_title_class = 'col-lg-9new'
link_class = 'mrmob5'
job_description_class = 'job-description'
apply_button_class = 'job-apply-single'
job_details_class = 'mt5'
filter_button_class = 'filterlist'
workex_filter_class = 'selectBox-dropdown'
workex_chooser_class = 'selectBox-dropdown-menu'
title_class = 'jdhding'
hastag_class = 'list-inline'
click_apply_id = 'job-apply-single'
applyjobid = 'applyJob'

output_file  = './../Output/IIMJOBS.csv'

#
# Gets data for the job opening
#
def get_details_of_opening(driver):

    # Declaring variables
    jd = ''
    job_title = ''
    hashtag = ''
    last_login = ''
    postedBy = ''
    postedIn = ''
    jobCode = ''
    Location = ''
    postedOn = ''
    views = ''
    applications = ''
    position = ''
    recruiterAction = ''

    jd = functions.find_class(driver, job_description_class).text

    job_title = functions.find_class(driver, title_class).text

    hashtag = functions.find_class(driver, hastag_class).text

    elements =  functions.find_classes(driver, job_details_class)
    for element in elements:
        try:
            sections = element.text.split('\n')
            if(sections[0] == 'Last Login:'):
                last_login = sections[1]
            elif(sections[0] == 'Posted by'):
                postedBy = sections[1]
                position = sections[2]
            elif(sections[0] == 'Posted in'):
                postedIn = sections[1]
            elif(sections[0] == 'Job Code'):
                jobCode = sections[1]
            elif(sections[0] == 'Location'):
                Location = sections[1]
            elif(sections[0] == 'Posted On'):
                postedOn = sections[1]
            elif(sections[0] == 'Views'):
                views = sections[1]
            elif(sections[0] == 'Applications'):
                applications = sections[1]
            elif(sections[0] == 'Recruiter Actions (what does this mean?)'):
                recruiterAction = sections[1]
            else:
                continue

        except:
            continue

        print(element)


    dict_data.append({'Job Code': jobCode, 'Title': job_title,'Hashtag': hashtag,'Description': jd,'Last Login': last_login, 'Posted By': postedBy,'Position': position,'Posted In': postedIn,'Location': Location,'Views': views,'Applications': applications,'Recruiter Actions': recruiterAction})

    functions.write_to_csv(output_file, dict_data, csv_columns)

    return 1

#
# makes the application for the portal
#
def make_application(driver):
    try:
        functions.find_id(driver, click_apply_id).click()
        functions.timeout(3)
        functions.find_id(driver, applyjobid).click()
        functions.timeout(3)
    except:
        return


#
# Checks whether the given is a job or ad
#
def check_if_job(element):
    if (functions.find_class(element, save_later_class) != None ):
        return True
    else:
        return False

#
# Applying for the job
#
def apply_for_the_job(driver, iter):
    if(iter >= iter_max):
        return
    else:
        item = 1

        elements = functions.find_classes(driver,job_row_class)
        for element in elements:
            if (check_if_job(element)):
                item = item + 1
                try:
                    print('Opening new job tab')
                    functions.open_in_new_tab(functions.find_class(element, link_class), driver)

                    functions.timeout(2)

                    print('Going to new window')
                    driver.switch_to_window(driver.window_handles[iter +1])

                    functions.timeout(2)

                    print('Getting details of the job')
                    get_details_of_opening(driver)

                    # Apply for the jobs
                    make_application(driver)

                    # Go into iteration
                    apply_for_the_job(driver, iter + 1)

                    print('closing the job')
                    functions.close_browser(driver)

                    #switch back to original window
                    functions.timeout(2)

                    print('going to prev window')
                    driver.switch_to_window(driver.window_handles[iter])
                except:
                    item = item - 1

            if(iter == 0 and item >10 ):
                break

    return 0

#
# Applies the filter of work ex
#
def apply_filter(driver):
    functions.find_classes(driver, workex_filter_class)[1].click()
    dropdown_menu = functions.find_class(driver, workex_chooser_class)
    functions.find_x_path(dropdown_menu, "//a[@rel='1']").click()
    functions.find_class(driver, filter_button_class).click()
    functions.timeout(2)

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
    functions.timeout(3)

    print('Applying filters to the website')
    apply_filter(driver)


    apply_for_the_job(driver, 0)

    # Download the data


    # List of skills required sheet

    # Close the browser

    functions.quit_browser(driver)

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    final_output = output_file + ' iimjobs '+ dt_string
    functions.write_to_csv(final_output, dict_data, csv_columns)
