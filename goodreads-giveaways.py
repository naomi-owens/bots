from splinter import Browser
from selenium import webdriver
import sys
import operator

def signIn(username, password):
	# Enter credentials
	browser.find_by_id('userSignInFormEmail').fill(username)
	browser.find_by_id('user_password').fill(password)
	browser.find_by_value('Sign in').click()	

def enterGiveaways(startPage):
	enteredTotal = 0
	giveawayPosition = 1
	currentPage = 1
	finished = False
	
	if startPage is not None:
		currentPage = startPage

	browser.visit('http://www.goodreads.com/giveaway')
	
	while not finished:
		print 'Page: ' + str(currentPage)
		
		if currentPage > 1:
			browser.visit('http://www.goodreads.com/giveaway?page=' + str(currentPage))	
	
		ul = browser.find_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul').first
		items = ul.find_by_tag('li')
		giveawaysOnPageCount = len(items)
	
		print 'Giveaways on page: ' + str(giveawaysOnPageCount)
	
		# Loop through all giveaways on page
		for x in range (1, giveawaysOnPageCount + 1):
			entered = False
			listItem = 'body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul > li:nth-child(' + str(giveawayPosition) + ') '
			giveawayActionsContainer = listItem + '> div.actions.giveawayPreviewDetailsContainer '
			giveawayDetailsContainer = listItem + '> div.giveawayPreviewBookContainer '
			giveawayStatus = giveawayActionsContainer  + '> div.mediumTextBottomPadded'
			
			giveawayTitleLink = giveawayDetailsContainer + '> div.description.descriptionContainer > a'
			element = browser.find_by_css(giveawayTitleLink).first
			href = element['href']
			d = {'key':'value'}
			
			giveawayAvailability = giveawayActionsContainer + '> div.sansSerif > p:nth-child(3)'
			availabilitySplit = browser.find_by_css(giveawayAvailability).first.text.split()
			# Convert fraction odds to implied probability percentage
			# Denominator / (Denominator + Numerator) * 100
			prob = float(availabilitySplit[1]) / (float(availabilitySplit[1]) + float(availabilitySplit[4])) * 100
			probabilityString = "%.2f" % round(prob,2)
			
			# set key and value
			d[href] = probabilityString
			
			if browser.is_element_present_by_css(giveawayStatus):
				mtbp = browser.find_by_css(giveawayStatus).first
				entered ='You are entered to win.' in mtbp.text
				
			if entered:
				# Already entered
				print str(x) + '. Already entered'
				giveawayPosition += 1
				
			elif browser.is_element_present_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul > li:nth-child(' + str(giveawayPosition) + ') > div.actions.giveawayPreviewDetailsContainer > div.mediumTextBottomPadded > a'):
				print str(x) + '. Entering...'
				# Click Enter Giveaway button
				button = browser.find_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul > li:nth-child(' + str(giveawayPosition) + ') > div.actions.giveawayPreviewDetailsContainer > div.mediumTextBottomPadded > a').first
				button.click()
			
				#Enter giveaway
				selectThisAddressButton = "//*[contains(text(), 'Select This Address')]"
				if browser.is_element_present_by_xpath(selectThisAddressButton):
					browser.find_by_xpath(selectThisAddressButton).first.click()
					browser.find_by_id('termsCheckBox').click()
					browser.find_by_id('giveawaySubmitButton').click()
					#Increment the total counter
					enteredTotal += 1
				
				#Else it must be a kindle book; do nothing for now and move to next book
				giveawayPosition += 1

				#Go back to all giveaways
				if currentPage > 1:
					browser.visit('http://www.goodreads.com/giveaway?page=' + str(currentPage))		
				else:
					browser.find_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.rightContainer > a').click();
		
			# It's the last giveaway on this page
			if x == giveawaysOnPageCount:
				print 'last giveaway on page'
				nextPageLinkPresent = browser.is_element_present_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > div.sansSerif > div > a.next_page')
				if nextPageLinkPresent:
					print 'next visible'
					currentPage += 1
					giveawayPosition = 1
				else:
					finished = True
	print 'Total Entered: ' + str(enteredTotal)
	sortedD = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
	print str(sortedD)

if len(sys.argv) < 3:
	print 'You must provide command args: email and password'
else:
	browser = Browser('chrome')
	browser.visit('http://www.goodreads.com')

	signIn(sys.argv[1], sys.argv[2])
	
	if len(sys.argv) > 3:
		enterGiveaways(int(sys.argv[3]))
	else:
		enterGiveaways(1)