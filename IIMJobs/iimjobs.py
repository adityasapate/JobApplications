import pandas
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

#
# Main function to start applying for jobs
#
if __name__ == "__main__":

    # Start chrome webdriver
    # driver = functions.open_browser(web_driver)

    # Retrieve login details
    login_details = functions.import_csv(login_details_location)
    for i in range (0,len(login_details)):
        if login_details.loc[i,'website'] == portal:
            loginid = login_details.loc[i,'loginid']
            password = login_details.loc[i,'password']

    print (loginid, password)

    # Open website


    # Apply for the job


    # Download the data


    # List of skills required sheet

    # Close the browser
    # functions.close_browser(driver)
