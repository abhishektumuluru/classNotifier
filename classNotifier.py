#!/usr/bin/env python

#A quick little script I wrote to automatically register me for classes
#so I don't have to watch BuzzPort and keep refreshing.
#Will have to be modified for Spring 2018 when two factor auth is mandatory

__author__ = "Abhishek Tumuluru"
__version__ = "1.0.0"
__email__ = "abhishek.tumuluru@gatech.edu"
__status__ = "It works"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

#see credentials.py for k,v pair username and pass 
import credentials
import time

class Course(object):
	#Nice way to contain necessary course information
	def __init__(self, subject, course_number):
		self.subject = subject
		self.course_number = course_number
	def __str__(self):
		return subject + " " + course_number
	def __repr__(self):
		return "Course({}, {})".format(self.subject, self.course_number)


SUBJECT = "CS"
LIST_COURSE_NUMS = ['4803']
courses_to_search = [Course(SUBJECT, courseNum) for courseNum in LIST_COURSE_NUMS]

my_username = credentials.username
my_password = credentials.password
MAX_TIMEOUT = 5
buzzport_url = r'https://login.gatech.edu/cas/login?service=http%3A%2F%2Fbuzzport.gatech.edu%2Fsso%3Bjsessionid%3D74561F2830B3A903ED312597BAF1F8DD'

#Let the browser remain in the global scope
#TODO make browser invisible i.e run in background
browser = webdriver.Chrome()

def login_buzzport():
	"""
	Log in to buzzport using the selenium driver.

	"""
	browser.get(buzzport_url)
	username = browser.find_element_by_id('username')
	username.send_keys(my_username)
	password = browser.find_element_by_id('password')
	password.send_keys(my_password)
	#click login button
	login_button = browser.find_element_by_name('submit')
	login_button.click()
	print("login successful")


def open_registration(courses_to_search, semester):
	"""
	Open buzzport registration and automatically fill in all necessary fields.
	Enter class id and attempt to register, even if there is no available space.

	Args:
	    courses_to_search (list): A list of Course objects.
	    semester (str): ex: "Fall 2017" or "Spring 2018". Whitespace necessary.
	"""
	WebDriverWait(browser, MAX_TIMEOUT).until(
    	EC.presence_of_element_located((By.XPATH, '//*[@id="u3649l1n118"]/div[2]/table/tbody/tr[1]/td[1]/div/p/a')))
	registration = browser.find_element_by_xpath('//*[@id="u3649l1n118"]/div[2]/table/tbody/tr[1]/td[1]/div/p/a')
	registration.click()
	print("student services opened")

	browser.get("https://oscar.gatech.edu/pls/bprod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
	browser.get("https://oscar.gatech.edu/pls/bprod/bwskfreg.P_AltPin")
	print("Add course search opened")

	term_dropdown = Select(browser.find_element_by_id("term_id"))
	term_dropdown.select_by_visible_text(semester)

	WebDriverWait(browser, MAX_TIMEOUT).until(
    	EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input')))
	submit = browser.find_element_by_xpath("/html/body/div[3]/form/input")
	submit.click()

	#try with CRNs for now. Switch to list of courses later
	crnEnter = browser.find_element_by_id("crn_id1")
	#testing with crn 86183
	crnEnter.send_keys("86183")


	submit = browser.find_element_by_xpath("/html/body/div[3]/form/input[19]")
	submit.click()
	print("tried registering")


def refresh():
	"""
	Refresh the page so the search can restart.
	"""
	browser.get(buzzport_url)


def main():
	"""
	Login and keep trying to register, allowing for loading times, sleeping
	so that BuzzPort doesn't think login attempts are an attack.
	"""
	login_buzzport()
	while True:
		try:
			open_registration(courses_to_search, "Fall 2017")
			time.sleep(5)
			refresh()
		except:
			login_buzzport()
			open_registration(courses_to_search, "Fall 2017")
			time.sleep(5)
			refresh()

if __name__ == '__main__':
	main()