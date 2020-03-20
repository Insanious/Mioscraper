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
	else:
		next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div[3]/div[2]/div[2]/div/a[2]')))
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

	return elements


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
		element = element[:-2] # remove first and second price
		#element = element[:-1] # remove second price

		# discount = ""
		# if new_price != -1:
		# 	element = element[:-1] # remove second price
		#
		# 	discount = element[-1]
		# 	element = element[:-1] # remove discount reason

		name = element[0]
		if len(element) > 2:
			name += ", "
			for sub in element[1:-1]: # extract the full name (including bloat if bloat doesn't contain any digits)
				name += sub + ", "
			name += element[-1]

		elif len(element) == 2:
			name += ", "
			name += element[1]

		new_element = {}
		new_element["name"] = name
		new_element["old_price"] = old_price

		if len(bloat) != 0:
			new_element["bloat"] = bloat
		if new_price != -1:
			new_element["new_price"] = new_price
			#new_element["discount"] = discount

		final.append(new_element)

	return final


def format_element(element, only_discounts):
	if only_discounts:
		if "new_price" not in element:
			return ""

	output = element["name"] + '\n'
	output += "old price: " + element["old_price"] + '\n'

	if "new_price" in element:
		output += "new price: " + element["new_price"] + '\n'
		output += f'diff %: {100 - (int(element["new_price"]) / int(element["old_price"]) * 100)}\n'
	if "bloat" in element:
		output += element["bloat"] + '\n'
	output += '\n'

	return output


def main():
	page_nr = 1
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)
	#driver = webdriver.Firefox()
	driver.implicitly_wait(1000)
	driver.get("https://www.mio.se/hela-sortimentet")

	total = []

	with open("output.txt", 'w+') as file:
		pass

	only_discount = True
	first = True

	while True:
		if first:
			first = False

			try:
				print(f"page nr: {page_nr}")

				elements = extract_discount_on_page(driver)
				elements = [ e.split('\n') for e in elements ]
				elements = [ e for e in elements if len(e) > 1 ]
				elements = filter_elements(elements)

				with open("output.txt", 'a') as file:
					for element in elements:
						file.write(format_element(element, only_discount))

			except:
				print("no fucking content")
				break
			finally:
				go_to_next_page(driver, True)
				page_nr += 1

		else:
			try:
				if page_nr > 10:
					break

				print(f"page nr: {page_nr}")

				elements = extract_discount_on_page(driver)
				elements = [ e.split('\n') for e in elements ]
				elements = [ e for e in elements if len(e) > 1 ]
				elements = filter_elements(elements)

				with open("output.txt", 'a') as file:
					for element in elements:
						file.write(format_element(element, only_discount))
			except:
				print("no fucking content")
				break
			finally:
				go_to_next_page(driver, False)
				page_nr += 1

	# total = [ e.split('\n') for e in total ]
	# total = [ e for e in total if len(e) > 1 ]

	# total.append(['New York', 'Kontinentalsäng, dubbelsäng med bäddmadrass', 'SPECIALPRIS', '9.995·', '12.995·', 'Se tillgänglighet'])
	# total.append(['Harper XL', '3-sits soffa XL', 'SPECIALPRIS', '13.495·', '14.995·', 'Se tillgänglighet'])
	# total.append(['Roma', 'Kontinentalsäng, dubbelsäng med bäddmadrass', 'SPECIALPRIS', '8.995·', '9.995·', 'Se tillgänglighet'])
	# total.append(['Roma', 'Ramsäng, enkelsäng med bäddmadrass', 'SPECIALPRIS', '3.995·', '4.495·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Charlotte', 'Stol', '1.695·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Tracy', 'Stol', '499·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Jack', 'Stol', '699·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Ekerö', 'Matbord, L 230 cm', '8.495·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Leon', 'Stol', '999·', 'Se tillgänglighet'])
	# total.append(['Upp till 5.000:- rabatt', 'Chatham', 'Stol', '899·', 'Se tillgänglighet'])
	#
	# total.append(['Napoli', 'Kontinentalsäng, dubbelsäng med bäddmadrass', '7.995·', 'Se tillgänglighet'])
	# total.append(['Fjällbacka', 'Kontinentalsäng, enkelsäng med bäddmadrass', '10.990·', 'Se tillgänglighet'])
	# total.append(['Leone', '3-sits soffa med divan höger', '17.990·', 'Se tillgänglighet'])
	# total.append(['Nevada', '3-sits soffa med divan vänster', '5.995·', 'Se tillgänglighet'])
	# total.append(['Napoli', 'Kontinentalsäng, enkelsäng med bäddmadrass', '5.995·', 'Se tillgänglighet'])
	# total.append(['County', '3-sits soffa', '6.295·', 'Se tillgänglighet'])
	# total.append(['Sleep Delux', 'Bäddmadrass', '3.195·', 'Se tillgänglighet'])
	# total.append(['Nevada', '3-sits soffa med schäslong vänster och divan höger', '6.995·', 'Se tillgänglighet'])
	# total.append(['Alfa', 'Nackkudde', '699·', 'Se tillgänglighet'])
	# total.append(['Nevada', '3-sits soffa med divan höger', '5.995·', 'Se tillgänglighet'])
	# total.append(['Palace', 'Hotellkudde 50x90 cm', '299·', 'Se tillgänglighet'])


	# final = filter_elements(total)
	#
	# for elem in final:
	# 	print(format_element(elem))

	print("done")

	driver.close()

if __name__ == "__main__":
	main()
