from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
import os
import json
import pandas as pd
import time
start_time = time.time()

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
chrome_path = os.path.realpath('chromedriver')
print(chrome_path)
browser = webdriver.Chrome(executable_path=chrome_path, options=option)


states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

allWaterSystems = []
waterSystem = []
counter = 0
currentEntry = 0
stateCounter = 0
noCity = 0
nextPage = False
providedCity = True
state = states[stateCounter]


for state in states:
    currentEntry = 0
    print(state)
    # Go to desired website

    browser.get("https://enviro.epa.gov/enviro/sdw_query_v3.get_list?wsys_name=&fac_search=fac_beginning&fac_county=&fac_city=&pop_serv=500&pop_serv=3300&pop_serv=10000&pop_serv=100000&pop_serv=100001&sys_status=active&pop_serv=&wsys_id=&fac_state=" +
                state+"&last_fac_name=&page=1&query_results=&total_rows_found=")

    try:
        alert = browser.switch_to_alert()
        alert.dismiss()
        time.sleep(1)
    except:
        print("No Alert")

    # Wait 20 seconds for page to load
    timeout = 20
    try:
        print('good')
        # Wait until the final element [Avatar link] is loaded.
        # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
        # the last things to be loaded.
        #WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='avatar width-full height-full rounded-2']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    # Get all of the titles for the pinned repositories
    # We are not just getting pure titles but we are getting a selenium object
    # with selenium elements of the titles.

    # find_elements_by_xpath - Returns an array of selenium objects.
    # Getting the totalEntries for Community Water System
    totalEntries = browser.find_elements_by_xpath(
        "//div[@class='dataTables_info']")
    totalEntries = totalEntries[0].text
    totalEntries = totalEntries.split(" ")
    totalEntries = totalEntries[-2]
    td = browser.find_elements_by_xpath("//td")
    totalEntries = totalEntries.replace(',', '')
    print(totalEntries)
    while(currentEntry != int(totalEntries)):
        for x in td:
            if(counter == 6):
                waterSystem.append(x.text)
                waterSystem.append(providedCity)
                if(providedCity == False):
                    waterSystem.append(False)

                allWaterSystems.append(waterSystem)
                nextPage = False
                waterSystem = []
                counter = 0
                currentEntry += 1
                print(currentEntry)
                providedCity = True
                if(currentEntry == int(totalEntries)):
                    break
                continue
            if(len(allWaterSystems) % 10 == 0 and len(allWaterSystems) != 0 and nextPage == False):
                link = browser.find_element_by_link_text('Next')
                browser.execute_script("arguments[0].click();", link)
                td = browser.find_elements_by_xpath("//td")
                nextPage = True
                break
            else:
                if(counter == 2 and x.text == 'NOT REPORTED'):
                    providedCity = False
                    noCity += 1
                if(counter == 2 and x.text != 'NOT REPORTED'):
                    cityname = x.text.split("\n")
                    waterSystem.append(cityname)
                    counter += 1
                else:
                    waterSystem.append(x.text)
                    counter += 1


print("Percetage of No cities provided")
print(noCity/len(allWaterSystems))


print("Total Time: ", time.time() - start_time)
