from splinter import Browser
import sys

def signIn(username, password):
	# Enter credentials
	browser.find_by_id('userSignInFormEmail').fill(username)
	browser.find_by_id('user_password').fill(password)
	browser.find_by_value('Sign in').click()	

def enterGiveaways():
	giveawayPosition = 1
	currentPage = 1
	finished = False

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
			
			if browser.is_element_present_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul > li:nth-child(' + str(giveawayPosition) + ') > div.actions.giveawayPreviewDetailsContainer > div.mediumTextBottomPadded'):
				mtbp = browser.find_by_css('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.content620 > ul > li:nth-child(' + str(giveawayPosition) + ') > div.actions.giveawayPreviewDetailsContainer > div.mediumTextBottomPadded').first
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
				browser.find_by_id('addressSelect2460766').click()
				browser.find_by_id('termsCheckBox').click()
				browser.find_by_id('giveawaySubmitButton').click()
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

if len(sys.argv) < 3:
	print 'You must provide command args: email and password'
else:
	browser = Browser('chrome')
	browser.visit('http://www.goodreads.com')
	signIn(sys.argv[1], sys.argv[2])
	enterGiveaways()
	