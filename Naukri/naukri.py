from logging import logThreads
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
website = 'https://www.naukri.com/jobs-in-mumbai?l=Mumbai%2C%20Mumbai%20Suburbs%2C%20Navi%20Mumbai%2C%20Mumbadevi%20Area%20-%20Mumbai%2C%20Mumbai%20Central%20-%20Mumbai%2C%20Mumbra%20-%20Mumbai'
login_details_location = './../../../Backup/login_details.csv'
portal = 'NAUKRI'
login_id = ''
password = ''

csv_columns =['Job Code', 'Title', 'Hashtag', 'Description', 'Last Login', 'Posted By', 'Position', 'Posted In', 'Location', 'Views', 'Applications', 'Recruiter Actions']
dict_data = []

iter_max = 3 #how deep do you want to go in the loop

login_placeholder_text = 'Enter your active Email ID'
password_placeholder_text = 'Enter your password'
submit_button_class = ''
login_button_class = 'login_Layer'

job_cluster_class = ''
job_row_class = ''
save_later_class = ''
job_title_class = ''
link_class = ''
job_description_class = ''
apply_button_class = ''
job_details_class = ''
filter_button_class = ''
workex_filter_class = ''
workex_chooser_class = ''
title_class = ''
hastag_class = ''
click_apply_id = ''
applyjobid = ''

output_file  = './../Output/IIMJOBS'

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
                # print('Location: ', Location)
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

    outfile = output_file + '.csv'
    dict_data.append({'Job Code': jobCode, 'Title': job_title,'Hashtag': hashtag,'Description': jd,'Last Login': last_login, 'Posted By': postedBy,'Position': position,'Posted In': postedIn,'Location': Location,'Views': views,'Applications': applications,'Recruiter Actions': recruiterAction})

    functions.write_to_csv(outfile, dict_data, csv_columns)

    return 1

#
# makes the application for the portal
#
def make_application(driver):
    try:
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
    functions.find_classes(driver, workex_filter_class)[1].click()
    dropdown_menu = functions.find_class(driver, workex_chooser_class)
    functions.find_x_path(dropdown_menu, "//a[@rel='2']").click()
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
    
    
    # Clicking on the login button
    functions.find_id(driver, login_button_class).click()

    functions.timeout(2)

    login_location = functions.find_class(driver, 'login-layer')

    lg = functions.find_classes(login_location, 'form-row')
    check = 1
    for l1 in lg:
        # if(check == 1):
        #     print('hello',l1.text)
        #     check = check + 1
        functions.find_x_path(l1, '//input').send_keys(login_id)
        # print('hello',l1.get_attribute('innerHTML'))
    # print('hello world',lg.text)
    # login_location.send_keys(login_id)
    


    


    # driver = functions.login_function(driver, login_placeholder_class, loginid, password_placeholder_class, password)
    
    functions.timeout(10)

    # print('Applying filters to the website')
    # apply_filter(driver)


    # apply_for_the_job(driver, 0)

    # Download the data


    # List of skills required sheet

    # Close the browser

    functions.quit_browser(driver)

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    final_output = output_file + ' iimjobs '+ dt_string + '.csv'
    functions.write_to_csv(final_output, dict_data, csv_columns)
