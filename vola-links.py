#DEPRECATED
#Use volafile python library
# from bs4 import BeautifulSoup
import requests
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys
delay = 10
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
start_url = "https://volafile.org/r/" + sys.argv[1]
wait = WebDriverWait(driver, 100)
driver.get(start_url)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'filelist_file')))
#r = driver.find_element_by_id("file_list")

def decision(size):
	if re.match(".* Byte$", size) or re.match(".* KB$",size):
		return False
	elif re.match(".* GB$", size):
		num = float(size.replace(" GB", ''))
		if num > 5:
	 		return False
		else:
			return True
	elif re.match(".* MB$", size):
		num = float(size.replace(" MB", ''))
		if num > 200:
	 		return True
		else:
			return False		
		return True	
	else:
		print("Size format not recognized.")
		raise
def expire_date(expire):
	e = datetime.datetime.now() + datetime.timedelta(minutes = expire)
	return int((e - datetime.datetime(1970,1,1)).total_seconds())

#Translate to minutes before deletion
def expire(time):
	if re.match(".* days$", time):
		expire = float(time.replace(" days", '')) * 24 * 60
	elif re.match(".* day$", time):
		expire = float(time.replace(" day", '')) * 24 * 60		
	elif re.match(".* hours$", time):
		expire = float(time.replace(" hours", '')) * 60
	elif re.match(".* hour$", time):
		expire = float(time.replace(" hour", '')) * 60		
	elif re.match(".* min$", time):
		expire = float(time.replace(" min", ''))
	else:
		print("Expiration not recognized.")	
		print("Expiration: ", time)
		raise
	return expire	

for elm in driver.find_elements_by_css_selector(".filelist_file")[::-1]:

	#### Expiration, Size
	# r = elm.find_element_by_class_name("file_right_part").text
	# q = elm.find_element_by_class_name("file_status").text

	# #q = elm.find_element_by_xpath("//span [@class='file_status']").text
	# size = r.replace(q,'')
	# time = q
	# exptime = expire(time)
	# expdate = expire_date(exptime)
	# dsize = decision(size)
	# #### URL, filename, 
	l = elm.find_element_by_class_name("file_left_part")
	# n = elm.find_element_by_class_name("file_name").text
	
	link = l.get_attribute('href')
	print(link)
driver.quit()





# 	r = elm.find_elements_by_css_selector(".file_left_part")
# 	print(r)
	#driver.findElement(By.Name("loginid"))
	# print(elm)
	
    #print(elm.find_elements_by_css_selector(".file_left_part")elm.text)
# for elm in driver.find_elements_by_css_selector(".file_left_part"):
# 	# r = elm.find_elements_by_css_selector(".file_left_part")
# 	#driver.findElement(By.Name("loginid"))
# 	# print(elm)
# 	print(elm.get_attribute('href'))
#     #print(elm.text)


