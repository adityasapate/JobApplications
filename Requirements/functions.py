import time
from random import randint
import csv
from selenium import webdriver
from random import *
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

#
# Global Variables
#
export_location = './../Output'

#
# Sleep for the specified time
#
def timeout(time_period):
    time.sleep(time_period)


#
# Opens the browser
#
def open_browser(web_driver):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(web_driver, options=options)
    return driver

#
# Wtite into the class
#
def write_into_class(driver, id_name, text):
    location = driver.find_element_by_id(id_name)
    location.send_keys(text)

#
# Wtite into the class
#
def login_function(driver, id_loc, id, password_loc, password):
    location = driver.find_element_by_id(id_loc)
    location.send_keys(id)
    location = driver.find_element_by_id(password_loc)
    location.send_keys(password+Keys.ENTER)
    return driver

#
# Find element by class name
#
def find_class(driver, class_name):
    return driver.find_element_by_class_name(class_name)

#
# Find element by class name
#
def find_classes(driver, class_name):
    return driver.find_elements_by_class_name(class_name)

#
#Finds links based on partial texts
#
def find_partial_text(driver, text):
    return driver.find_element_by_partial_link_text(text)

#
#Finds links based on partial texts
#
def find_partial_texts(driver, text):
    return driver.find_elements_by_partial_link_text(text)


#
# Finds the element by xpath
#
def find_x_path(driver, path):
    return driver.find_element_by_xpath(path)

#
# Find element by class name
#
def find_id(driver, id_name):
    return driver.find_element_by_id(id_name)


#
# Open Link in new TAB
#
def open_in_new_tab(element, driver):
    action = ActionChains(driver)
    action.key_down(Keys.COMMAND).click(element).key_up(Keys.COMMAND).perform()

#
# Find element by class name
#
def find_class_text(driver, class_name):

    return driver.find_element_by_class_name(class_name).text

#
# Goto New tab
#
def right_tab(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL , Keys.TAB)

#
# Press 2 keys
#
def press_2_keys(driver, key1, key2):
    actions = ActionChains(driver)
    actions.key_down(key1).key_down(key2).key_up(key2).key_up(key1).perform()

#
# Press 2 keys
#
def find_tag(element, tag):
    element.find_elements_by_tag_name(tag)

#
# Closes the driver
#
def close_browser(driver):
    driver.close()


#
# Closes the driver
#
def quit_browser(driver):
    driver.quit()


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

#
# Write to the file
#
def write_to_csv(csv_file, dict_data, csv_columns):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")


#
# Main Window
#
if __name__== "__main__":
    main()
