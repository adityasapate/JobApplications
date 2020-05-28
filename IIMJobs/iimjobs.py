import pandas
# some_file.py
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


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

iter_max = 3 #how deep do you want to go in the loop

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





#
# Gets data for the job opening
#
def get_details_of_opening(driver):
    jd = functions.find_class(driver, job_description_class).text
    print (jd)

    elements =  functions.find_classes(driver, job_details_class)
    for element in elements:
        print (element.text)





    return 1



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
    if(iter >= 3):
        print("hello")
        return
    else:
        item = 1

        elements = functions.find_classes(driver,job_row_class)
        for element in elements:
            print
            print (element.text)
            if (check_if_job(element)):
                item = item + 1
                try:
                    functions.open_in_new_tab(functions.find_class(element, link_class), driver)

                    print(functions.find_class(element, link_class).get_attribute('href'))


                    # functions.open_in_new_tab(functions.find_tag(element, "a"), driver)
                    # print(functions.find_tag(element,"a").get_attribute('href'))
                    functions.timeout(2)

                    driver.switch_to_window(driver.window_handles[iter +1])
                    print("bab")
                    functions.timeout(2)
                    # get_details_of_opening(driver)
                    # get_details_of_opening(driver)

                    # Apply for the jobs


                    apply_for_the_job(driver, iter + 1)

                    functions.close_browser(driver)
                    #switch back to original window
                    functions.timeout(2)

                    driver.switch_to_window(driver.window_handles[iter])
                except:
                    item = item -1 

            if(iter == 0 and item >3 ):
                break



    return 0



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

    # Login into the website
    driver = functions.login_function(driver, login_placeholder_class, loginid, password_placeholder_class, password)
    functions.timeout(5)

    apply_for_the_job(driver, 0)

    # Download the data


    # List of skills required sheet

    # Close the browser

    functions.quit_browser(driver)
