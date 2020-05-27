import time
from random import randint
import csv
from selenium import webdriver
from random import *
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time

#
# Sleep for the specified time
#
def timeout(time_period):
    time.sleep(time_period)

#
# Global Variables
#
export_location = './../Output'

#
# Opens the browser
#
def open_browser(web_driver):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(web_driver, options=options)
    return driver

#
# Closes the driver
#
def close_browser(driver):
    driver.close()

#
# Import the data from provided CSV
#
def import_csv(csv_file):
    return pd.read_csv(csv_file)

#
# Exports file to CSV
#
def export_csv(df, output_type, location):
    output = export_location + output_type + "/" +export_location + "/"
    export_csv = df.to_csv (output, index = None, header=True) #Don't forget to add '.csv' at the end of the path

if __name__== "__main__":
    main()
