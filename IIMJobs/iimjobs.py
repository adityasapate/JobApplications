import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, './../Requirements/') # path of the file where the requirements file 1. edge driver and 2. functions file

import functions

# Global Variables
web_driver = "./../Requirements/msedgedriver" # Location of the webdriver
website = 'https://www.iimjobs.com' # Website that I want to login
portal = 'IIMJOBS' # this is a folder name and identifier
login_details_location = './../../../Backup/login_details.csv' # Details of the login are saved in this file 
login_id = '' # variable for getting the login id
password = '' # variable for getting the login password

# Data structure to save the file
csv_columns =['Job Code', 'Title', 'Hashtag', 'Description', 'Last Login', 'Posted By', 'Position', 'Posted In', 'Location', 'Views', 'Applications', 'Recruiter Actions']
dict_data = []

iter_max = 3 #how deep do you want to go in the loop

# Identifier for login page
login_placeholder_class = 'large-email' 
password_placeholder_class = 'large-password'
submit_button_class = 'button-submit'

# Identifier for the filter button
workex_chooser_class = 'selectBox-dropdown-menu'
workex_filter_class = 'selectBox-dropdown'
filter_button_class = 'filterlist'

# Check element class if it is a job
save_later_class = 'saved-job'

# This is the parent class of the job elements, we will iterate through this class
job_row_class = 'jobRow'

# This is the link associated with the jobs
link_class = 'mrmob5'

# Classes to find the details of the job 
job_description_class = 'job-description'
title_class = 'jdhding'
job_details_class = 'mt5'
hastag_class = 'list-inline'

# The classes to skip video resume
pop_up_video_resume_class = 'round-zero_remindlater'
skip_video_resume_application = 'rz-skip-btn'
skip_video_remume_application_anyway = 'skip-anyway-btn'

# Apply for the job
click_apply_id = 'job-apply-single'
applyjobid = 'applyJob'

# Output file location
output_file  = './../Output/IIMJOBS'
outfile = ''

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
    dt_string = '' # The file name in which the

    jd = functions.find_class(driver, job_description_class).text
    # print('The job id is: ', jd)

    job_title = functions.find_class(driver, title_class).text
    # print('The job title is: ', job_title)

    hashtag = functions.find_class(driver, hastag_class).text

    elements =  functions.find_classes(driver, job_details_class)
    for element in elements:
        try:
            sections = element.text.split('\n')
            if(sections[0] == 'Last Login:'):
                last_login = sections[1]
                # print('Last Login: ',last_login)
            elif(sections[0] == 'Posted by'):
                postedBy = sections[1]
                # print('Posted by: ', postedBy)
                position = sections[2]
                # print('Position: ', position)
            elif(sections[0] == 'Posted in'):
                postedIn = sections[1]
                # print('Posted In: ', postedIn)
            elif(sections[0] == 'Job Code'):
                jobCode = sections[1]
                # print('Job Code: ', jobCode)
            elif(sections[0] == 'Location'):
                Location = sections[1]
                print('Location: ', Location)
            elif(sections[0] == 'Posted On'):
                postedOn = sections[1]
                # print('Posted On', postedOn)
            elif(sections[0] == 'Views'):
                views = sections[1]
                # print('Views: ', views)
            elif(sections[0] == 'Applications'):
                applications = sections[1]
                # print('Applications: ', applications)
            elif(sections[0] == 'Recruiter Actions (what does this mean?)'):
                recruiterAction = sections[1]
                # print('Recruiter Actions (what does this mean?)', recruiterAction)
            else:
                continue

        except:
            continue

        # print(element)

    dict_data.append({'Job Code': jobCode, 'Title': job_title,'Hashtag': hashtag,'Description': jd,'Last Login': last_login, 'Posted By': postedBy,'Position': position,'Posted In': postedIn,'Location': Location,'Views': views,'Applications': applications,'Recruiter Actions': recruiterAction})
    functions.write_to_csv(outfile, dict_data, csv_columns)

    return 1

#
# makes the application for the portal
#
def make_application(driver):
    try:
        print('Skipping the video resume')
        try:
            functions.find_class(driver, skip_video_resume_application).click()
            functions.timeout(2)
            functions.find_class(driver, skip_video_remume_application_anyway).click()
            functions.timeout(2)
            
        except:
            functions.timeout(2)
        
        functions.find_id(driver, click_apply_id).click()
        functions.timeout(5)
        functions.find_id(driver, applyjobid).click()
        functions.timeout(5)
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
# Check the pop up of video resume
# 
def skip_video_resume_pop_up(driver):
    try:
        functions.find_class(driver, pop_up_video_resume_class).click()
    except:
        return 1


#
# Applying for the job
#
def apply_for_the_job(driver, iter):
    if(iter >= iter_max):
        return
    else:
        item = 1

        # Skip the pop up video resume class
        skip_video_resume_pop_up(driver)
        print('Skipping video login')
        functions.timeout(5)

        # Find elements of the job
        elements = functions.find_classes(driver,job_row_class)
        # Iterate over the job elements 
        for element in elements:
            if (check_if_job(element)):
                item = item + 1
                try:
                    print('Opening new job tab')
                    
                    functions.open_in_new_tab(functions.find_class(element, link_class), driver)

                    functions.timeout(2)

                    print('The current window handle: ', driver.current_window_handle)
                    print("Value of iterator is: ", iter)
                    print('the value of item is:', item)

                    print('Going to new window')
                    driver.switch_to.window(driver.window_handles[iter+1])
                    print('The next window handle: ', driver.current_window_handle)

                    
                    # functions.timeout(2)

                    print('Getting details of the job')
                    get_details_of_opening(driver)

                    # Apply for the jobs
                    print('Applying for job')
                    make_application(driver)

                    # Go into iteration
                    apply_for_the_job(driver, iter + 1)

                    print('closing the job')
                    functions.close_browser(driver)

                    #switch back to original window
                    functions.timeout(2)

                    print('going to prev window')
                    driver.switch_to.window(driver.window_handles[iter])
                except:
                    item = item - 1

            if(item >10):
                break

    return 0

#
# Applies the filter of work ex 
#
def apply_filter(driver):

    # This will select the number of days of workex that the candidate has 
    functions.find_classes(driver, workex_filter_class)[1].click()
    dropdown_menu = functions.find_class(driver, workex_chooser_class)
    functions.find_x_path(dropdown_menu, "//a[@rel='2']").click()

    # This will select the location suitable for the candidate
    functions.find_classes(driver, workex_filter_class)[2].click()
    
    functions.find_x_path(driver, '/html/body/div[3]/div[3]/div[9]/div[2]/div[2]/form/div[1]/div[3]/div/div[2]/div[49]/div/input').click()
    functions.find_x_path(driver, '/html/body/div[3]/div[3]/div[9]/div[2]/div[2]/form/div[1]/div[3]/div/div[2]/div[53]/div/input').click()
    
    functions.find_class(driver, filter_button_class).click()
    functions.timeout(2)

#
# Main function to start applying for jobs
#
if __name__ == "__main__":

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    outfile = output_file + ' iimjobs ' + dt_string + '.csv'


    # Start chrome webdriver
    driver = functions.open_browser(web_driver)

    # Retrieve login details
    print("Getting details of ID and password")
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

    print('Starting application for the jobs')
    apply_for_the_job(driver, 0)

    # Download the data

    # List of skills required sheet

    # Close the browser
    functions.quit_browser(driver)

    