from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import *

from time import sleep


def go_to_next_page(driver, is_first):
	next_button = None
	if is_first:
		next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div[3]/div[2]/div[2]/div/a')))
		#next_button = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/div[2]/div[2]/div/a')
	else:
		next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div[3]/div[2]/div[2]/div/a[2]')))
		#next_button = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/div[2]/div[2]/div/a[2]')
	next_button.click()


def extract_discount_on_page(driver):
	sleep(2)
	elements = []
	for i in range(1, 26):
		wait = WebDriverWait(driver, 1000)
		try:
			element = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="app"]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[{i}]')))
		except NoSuchElementException:
			print("NoSuchElementException")
			continue
		except StaleElementReferenceException:
			print("StaleElementReferenceException")
			continue
		except:
			print("unexpected")
		finally:
			text = ""
			text += element.text
			elements.append(text)
	#elements = [ WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="app"]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[{i}]'))) for i in range(1, 26) ]

	#discounted = [ elem.text for elem in elements if elem.text.find("SPECIALPRIS") != -1 ]

	return elements

	formatted = []
	for elem in discounted:
		old_price, new_price = (elem[-2][:-1], elem[-3][:-1]) if elem[-1] == "Se tillgänglighet" else (elem[-1][:-1], elem[-2][:-1])
		name = elem[0] + " "
		for field in elem[1:]:
			if (field == "SPECIALPRIS"):
				break
			name += field

		formatted.append([name, old_price, new_price])

	return formatted


def is_price(element):
	element = element.replace('·', '')
	element = element.replace('.', '')
	return element if element.isdigit() else -1


def contains_digit(element):
	return any(char.isdigit() for char in element)


def filter_elements(elements):
	final = []

	for element in elements:
		if is_price(element[-1]) == -1: # remove shit in the back
			element = element[:-1]

		new_price = is_price(element[-2]) # extract new price

		bloat = ""
		if contains_digit(element[0]): # remove bloat in front
			bloat = element[0]
			element = element[1:]

		if new_price == -1 and len(bloat) == 0: # not a discounted item
			continue

		old_price = is_price(element[-1])
		element = element[:-1] # remove first price

		discount = ""
		if new_price != -1:
			element = element[:-1] # remove second price

			discount = element[-1]
			element = element[:-1] # remove discount reason

		name = element[0] + ", "
		for sub in element[1:]: # extract the full name (including bloat if bloat doesn't contain any digits)
			name += sub

		new_element = {}
		new_element["name"] = name
		new_element["old_price"] = old_price

		if len(bloat) != 0:
			new_element["bloat"] = bloat
		if new_price != -1:
			new_element["new_price"] = new_price
			new_element["discount"] = discount

		final.append(new_element)

	return final


def main():
	page_nr = 1
	options = Options()
	options.headless = True
	#driver = webdriver.Firefox(options=options)
	#driver = webdriver.Firefox()
	#driver.implicitly_wait(1000)
	#driver.get("https://www.mio.se/hela-sortimentet")

	total = []
	#elements = extract_discount_on_page(driver)
	#for e in elements:
	#	total.append(e)

	#go_to_next_page(driver, True)
	#page_nr += 1
	#print(f"page nr {page_nr}")


	# while True:
	# 	try:
	# 		elements = extract_discount_on_page(driver)
	# 		for e in elements:
	# 			total.append(e)
	# 			#print(e)
	# 	except:
	# 		print("no fucking content")
	# 		for e in total:
	# 			print(e)
	# 		break
	#
	# 	try:
	# 		if page_nr > 1:
	# 			break
	# 		go_to_next_page(driver, False)
	# 		page_nr += 1
	# 		print(f"page nr {page_nr}")
	# 	except:
	# 		print("no fucking button")
	# 		for e in total:
	# 			print(e)
	# 		break


	#total = [ e.split('\n') for e in total ]
	#total = [ e for e in total if len(e) > 1 ]

	total.append(['New York', 'Kontinentalsäng, dubbelsäng med bäddmadrass', 'SPECIALPRIS', '9.995·', '12.995·', 'Se tillgänglighet'])
	total.append(['Harper XL', '3-sits soffa XL', 'SPECIALPRIS', '13.495·', '14.995·', 'Se tillgänglighet'])
	total.append(['Roma', 'Kontinentalsäng, dubbelsäng med bäddmadrass', 'SPECIALPRIS', '8.995·', '9.995·', 'Se tillgänglighet'])
	total.append(['Roma', 'Ramsäng, enkelsäng med bäddmadrass', 'SPECIALPRIS', '3.995·', '4.495·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Charlotte', 'Stol', '1.695·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Tracy', 'Stol', '499·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Jack', 'Stol', '699·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Ekerö', 'Matbord, L 230 cm', '8.495·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Leon', 'Stol', '999·', 'Se tillgänglighet'])
	total.append(['Upp till 5.000:- rabatt', 'Chatham', 'Stol', '899·', 'Se tillgänglighet'])

	total.append(['Napoli', 'Kontinentalsäng, dubbelsäng med bäddmadrass', '7.995·', 'Se tillgänglighet'])
	total.append(['Fjällbacka', 'Kontinentalsäng, enkelsäng med bäddmadrass', '10.990·', 'Se tillgänglighet'])
	total.append(['Leone', '3-sits soffa med divan höger', '17.990·', 'Se tillgänglighet'])
	total.append(['Nevada', '3-sits soffa med divan vänster', '5.995·', 'Se tillgänglighet'])
	total.append(['Napoli', 'Kontinentalsäng, enkelsäng med bäddmadrass', '5.995·', 'Se tillgänglighet'])
	total.append(['County', '3-sits soffa', '6.295·', 'Se tillgänglighet'])
	total.append(['Sleep Delux', 'Bäddmadrass', '3.195·', 'Se tillgänglighet'])
	total.append(['Nevada', '3-sits soffa med schäslong vänster och divan höger', '6.995·', 'Se tillgänglighet'])
	total.append(['Alfa', 'Nackkudde', '699·', 'Se tillgänglighet'])
	total.append(['Nevada', '3-sits soffa med divan höger', '5.995·', 'Se tillgänglighet'])
	total.append(['Palace', 'Hotellkudde 50x90 cm', '299·', 'Se tillgänglighet'])


	final = filter_elements(total)

	'''
	ff len(bloat) != 0:
		new_element["bloat"] = bloat
	if new_price != -1:
		new_element["new_price"] = new_price
		new_element["discount"] = discount
	'''

	for elem in final:
		if "bloat" in elem:
			pass
		if "new_price" in elem:
			pass
			pass

	#driver.close()

if __name__ == "__main__":
	main()
