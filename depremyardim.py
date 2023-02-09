from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import json
import schedule
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
        sorted(district_with_provinces.items(), key=lambda item: item[1], reversed=True))
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

    for district in districts_all:
        district_txt = district.text

        district = district_txt[district_txt.find('/') + 2:]
        province = district_txt[0:  district_txt.find('/') - 1]
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

    district_with_provinces = dict(
        sorted(district_with_provinces.items(), key=lambda item: item[1], reverse=True))
    district_with_provinces["UPDATED AT:"] = updated_at

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

# class informations
district_province = "mt-2 text-sm font-bold text-slate-300"
timestamp_class = "mt-2 text-sm font-bold text-slate-400"
address_class = "text-sm font-medium text-white"
div_class = "relative px-4 py-4 bg-black hover:bg-gray-900 transition-all"
msg_class = "text-sm font-medium text-white"

districts_provinces_all = soup.find_all(
    'p', attrs={"class": district_province})
timestamp_scraped = soup.find_all(
    'p', attrs={"class": timestamp_class})
address_scraped = soup.find_all(
    'p', attrs={"class": address_class})
msg_scraped = soup.find_all(
    'p', attrs={"class": msg_class})
div_scraped = soup.find_all(
    'div', attrs={"class": div_class})

# ! plain text print
# for post_time in timestamp_scraped:
#     print(post_time.text)
# for div_data in div_scraped:
#     print(div_data.text)


fileName = open('adresler.txt', 'r+', encoding="utf8")

addresses = []
for msg_data in msg_scraped:
    fileName.write(msg_data.text)
    fileName.write("\n-----------\n")
fileName.close()

# Dict values
districts = {}
provinces = {}
district_with_provinces = {}

# Update depremzedeler.json

updateFile(districts, provinces,
           districts_provinces_all, district_with_provinces)

# Additional info can be found @https://github.com/dbader/schedule
schedule.every(3).minutes.do(updateFile)

while 1:
    schedule.run_pending()
    time.sleep(1)
    driver.quit()
driver.quit()
