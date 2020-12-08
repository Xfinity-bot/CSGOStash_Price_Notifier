#This project uses csgostash.com to fetch prices
#Eg input : https://csgostash.com/skin/1301/M4A1-S-Printstream
#For any enquiry mail us @  sriganesh7334@gmail.com

#importing modules csv,os,requests,selenium,bs4

from selenium import webdriver  
from bs4 import BeautifulSoup
import csv
import requests
import os

#Clearing screen
os.system('cls' if os.name == 'nt' else 'clear')


scondition=['FN','MW','FT','WW','BS'] #conditions possible for skins


#Function to clear the list after every loop
def clearvalues():
	global nskinp,stskinp,sskinp
	nskinp=[]
	stskinp=[]
	sskinp=[]


#initailising 	to null
nskinp=[]
stskinp=[]
sskinp=[]


# Taking url as input and setting up selenium
url = input("Enter CSGOSTASH skin url : " )
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


#Function to retrive prices of skin
def retriveprice():
	global nskinp,stskinp,sskinp,scondition 

	driver.get(url)
	htmlfile = driver.page_source  #getting html source using selenium 
	soup = BeautifulSoup(htmlfile ,'html.parser')  #passing it to bs4
	
	#Fetching the price using bs4 and aapending to the respective list depending on skin type

	for a in soup.findAll('a', attrs={'class':['btn btn-default btn-sm market-button-skin','btn btn-default btn-sm market-button-skin disabled-clickable','btn btn-default btn-sm market-button-skin disabled']}):

		if a.find('span', attrs={'class':'pull-right'}):
			price=a.find('span', attrs={'class':'pull-right'})
			if a.find('span', attrs={'class':'pull-left price-details-st'}):
				stskinp.append(price.contents)
			elif a.find('span', attrs={'class':'pull-left price-details-souv'}):
				sskinp.append(price.contents)
			else:
				nskinp.append(price.contents)


	#cleaning/Processing the data & converting string into into

	#Removing list of list
	nskinp=[''.join(x) for x in nskinp]
	stskinp=[''.join(x) for x in stskinp]
	sskinp=[''.join(x) for x in sskinp]

	#Removing ',' & '₹'  from price
	for c,itemprice in enumerate(nskinp):
		nskinp[c]=itemprice.replace(",", "").replace("₹","")
	for c,itemprice in enumerate(stskinp):
		stskinp[c]=itemprice.replace(",", "").replace("₹","")
	for c,itemprice in enumerate(sskinp):
		sskinp[c]=itemprice.replace(",", "").replace("₹","")


    #Writing the price to csv file
	with open('skin.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		#The skin prices are dependend on its type and a skin can have max of two types ,wrinting data depending on type using if
		if stskinp:
			
			writer.writerow(["Wear", "Regular","StatTrack"])


			print()
			print("Wear","Regular","StatTrack",sep="  ",end="\n\n")
			#Rowwise writing data into csv

			for count in range(len(nskinp)):
				
				temp=[]
				temp.append(scondition[count])
				temp.append(nskinp[count])
				temp.append(stskinp[count])
				writer.writerow(temp)

				print(scondition[count],nskinp[count],stskinp[count],sep="\t") #printing prices to screen
		elif sskinp:
			writer.writerow(["Wear", "Regular","Souvenir"])
			print()
			print("Wear","Regular","Souvenir",sep="  ",end="\n\n")

			for count in range(len(nskinp)):

				temp=[]
				temp.append(scondition[count])
				temp.append(nskinp[count])
				temp.append(sskinp[count])
				writer.writerow(temp)

				print(scondition[count],nskinp[count],sskinp[count],sep="\t")
		else:
			writer.writerow(["Wear", "Regular"])
			print()
			print("Wear","Regular",sep="  ",end="\n\n")


			for count in range(5):
				temp=[]
				temp.append(scondition[count])
				temp.append(nskinp[count])
				writer.writerow(temp)

				print(scondition[count],nskinp[count],sep="\t")
				
retriveprice()
print()			
print("###############################################", end="\n\n\n")

#asking user about notification until user enters yes or no
while True:
	print("Do you want to get notified when price drops ?. (Yes/No)")

	notifcondi=input().capitalize()
	if(notifcondi!="Yes" and notifcondi!="No"):
		continue
	else:
		break


os.system('cls' if os.name == 'nt' else 'clear')


#comparing the prices 
if notifcondi=="Yes" :
	currentprice=0
	#user will get notified to this mail
	#############   Note  ##############
	#The free plan of mailgun api (which we have used here)  are restricted to authorized recipients only and have limit of 5 !!

	buymail=input("Enter your mail address :  ") 
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Enter skin Type",end="\n\n")
	print("1 Regular","2 StatTrack","3 Souvenir","Eg: Enter 2 for StatTrack", sep="\n")
	buytype=int(input())
	os.system('cls' if os.name == 'nt' else 'clear')

	print("Enter the wear",end="\n\n")
	print("1  Factory New","2  Minimal Wear","3  Field Tested","4  Well Worn","5  Battle Scarred","Eg: Enter 1 for Factory New", sep="\n")
	buywear=int(input())
	os.system('cls' if os.name == 'nt' else 'clear')
	buyrequest=int(input("Enter the price : "))
	

    #Fetching price depending on skin-type provided by user
	if buytype==1:
		
		currentprice=nskinp[buywear-1]
	elif buytype==2:
		currentprice=stskinp[buywear-1]
	else :
		
		currentprice=sskinp[buywear-1]


	#Filtering not available and not feasible combinations and notifing user
	if currentprice!="No Recent Price" and currentprice!="Not Possible" :

		#Infinte loop checking for price drop
		while True:

			#comparing prices 
			if int(currentprice)<=buyrequest:
			    
				#Sending mail using mailgun api 
				def send_simple_message():
					return requests.post(
						"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
						auth=("api", "yourapikey"),
						data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
							"to": buymail,
							"subject": "Alert!!",
							"text": "Price Drop alert!!!!"})

				send_simple_message()
				print("Email has been sent!!") #notifing 

				break
			driver.refresh()  #refreshing page after every comparison
			clearvalues()     #resetting values of list
			retriveprice()	  #Retreiving price looop
	else:
		print("The entered combination is not possible or available. Please enter valid input")
else:
	print("Thank You for using our services")

driver.quit() 