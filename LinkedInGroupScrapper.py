import csv
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
# preparing csv file to store parsing result later
# csv file has to exist before hand in the same directory
writer = csv.writer(open('test.csv', 'w'))
writer.writerow(['Name', 'Schools', 'Location','Company','Position','Dates_Employed', 'Time_at_job,','connections','url'])
#this ensures the most updated driver is used
driver = webdriver.Chrome(ChromeDriverManager().install())
#log in user/password
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
driver.find_element_by_id('username').send_keys("###########")
driver.find_element_by_id('password').send_keys("###########")
#log in selector wait of 10 seconds to ensure automation passes
driver.find_element_by_class_name('login__form_action_container ').click()
driver.implicitly_wait(10)
driver.get('https://www.linkedin.com/groups/"group_code_here"/members/')
driver.execute_script("document.body.style.zoom='75%'")
#takes all elements and saves as int for profile count
profile_count = int(driver.find_element_by_class_name('groups-members-list').text[:4])
group = driver.find_element_by_class_name('groups-members-list__results-list')
elems = group.find_element_by_xpath("//a[@href]")

profiles = []

#logic
count = 0
while count < profile_count:
    count = 0
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    elems = group.find_elements_by_xpath("//a[@href]")
    #print('made it here')
    for elem in elems:
        #if "https://www.linkedin.com/in/" in elem.get_attribute("href"):
        count += 1
#if its a proper linkedin account add the url to the list of proifles
for elem in elems:
    if "https://www.linkedin.com/in/" in elem.get_attribute("href"):
        profiles.append(elem.get_attribute("href"))
#loop through each of the profiles in list
for i in range(2, len(profiles)):
    driver.get(profiles[i])
    driver.execute_script("document.body.style.zoom='15%'")
    time.sleep(5)
#paths to location of data on profile
    try:
        sel = Selector(text=driver.page_source)
        name = driver.find_element_by_class_name('pv-top-card--list').text.splitlines()[0]
        schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        company = driver.find_element_by_class_name('pv-top-card--experience-list').text.splitlines()[0]
        position = driver.find_element_by_css_selector("div.pv-entity__summary-info h3.t-16").text
        dates_employed = driver.find_element_by_css_selector("div.display-flex h4.pv-entity__date-range").text
        time_at_job = driver.find_element_by_css_selector("div.display-flex span.pv-entity__bullet-item-v2").text.splitlines()[0]
        url = driver.current_url
        connections = driver.find_element_by_css_selector("div.flex-1 span.t-16").text.splitlines()[0]
        #if information cant be located prints failed
    except:
        print('failed')
        schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        dates_employed = "NULL"
        time_at_job = "NULL"
        company = "NULL"
        position = "NULL"
        connections = "NULL"
        url = "NULL"
        location = "NULL"

    # print to console for testing purpose
    print('\n')
    print(name)
    print(schools)
    print(location)
    print(company)
    print(dates_employed)
    print(time_at_job)
    print(connections)
    print(url)
    print(position)
    print('\n')

    #writes to file AT END OF PROGRAM
    writer.writerow([name, schools, location, company,position,dates_employed, time_at_job, connections,url])
    del schools
    del location
    del company
    del position
    del dates_employed
    del time_at_job
    del url
    del connections

driver.quit()
print('finished')