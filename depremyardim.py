from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import json

url = 'https://www.depremyardim.org/'

# Create a new Chrome session
driver = webdriver.Chrome()
# Load the web page
driver.get(url)
# Wait for the page to fully load
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'lxml')

# scrool to the end of the page
lenOfPage = driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while (match == False):
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

# You can use this function as a sandbox
def setDistrictProvince(districts, provinces, districts_all, district_with_provinces):
    f = open('depremzedeler.json', 'a', encoding='utf-8')

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    today = date.today()
    f.write('\n')
    updated_at = str(today) + " " + str(current_time)
    district_with_provinces["UPDATED AT:"] = updated_at
    f.write('\n')

    for district in districts_all:
        file = district.text

        district = file[file.find('/') + 2:]
        province = file[0:  file.find('/') - 1]
        alias_format = province + " / " + district
        print(alias_format)
        if (district not in districts):
            districts[district] = 1

        if (province not in provinces):
            provinces[province] = 1
        # if (district not in provinces):
        #     provinces[district] = 1
        # if (district in provinces):
        #     provinces[district] += 1

        if (district in districts):
            districts[district] += 1
        if (province in provinces):
            provinces[province] += 1

        if (alias_format not in district_with_provinces):
            district_with_provinces[alias_format] = 1
        if (alias_format in district_with_provinces):
            district_with_provinces[alias_format] += 1

    district_with_provinces = dict(
        sorted(district_with_provinces.items(), key=lambda item: item[1], reverse=True))
    dwp = json.dumps(district_with_provinces,
                     ensure_ascii=False).encode('utf8')
    f.write(dwp.decode())
    f.write(',')
    f.write(str(district_with_provinces))
    f.write(str(district))
    f.write(str(provinces))


def updateFile(districts, provinces, districts_all, district_with_provinces):

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    today = date.today()
    updated_at = str(today) + " " + str(current_time)
    district_with_provinces["UPDATED AT:"] = updated_at

    for district in districts_all:
        file = district.text

        district = file[file.find('/') + 2:]
        province = file[0:  file.find('/') - 1]
        alias_format = province + " / " + district
        if (district not in districts):
            districts[district] = 1

        if (province not in provinces):
            provinces[province] = 1

        if (district in districts):
            districts[district] += 1
        if (province in provinces):
            provinces[province] += 1

        if (alias_format not in district_with_provinces):
            district_with_provinces[alias_format] = 1
        if (alias_format in district_with_provinces):
            district_with_provinces[alias_format] += 1

    dwp = json.dumps(district_with_provinces,
                     ensure_ascii=False).encode('utf8')

    with open('depremzedeler.json', 'r+', encoding="utf8") as file:
        # Load the existing data into a Python object
        data = json.load(file)
        # Modify the data as desired
        data.append(district_with_provinces)
        # Move the file pointer to the beginning of the file
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4, ensure_ascii=False)
        # Truncate the file to remove any extraneous data that may have been added
        file.truncate()

district_province = "mt-2 text-sm font-bold text-slate-300"
timestamp_clas = "mt-2 text-sm font-bold text-slate-400"

districts_provinces_all = soup.find_all(
    'p', attrs={"class": district_province})
timestamp_scraped = soup.find_all('p', attrs={"class": timestamp_clas})
timestamp = timestamp_scraped

# Dict values
districts = {}
provinces = {}
district_with_provinces = {}

# Update depremzedeler.json
updateFile(districts, provinces,
                    districts_provinces_all, district_with_provinces)

driver.quit()
