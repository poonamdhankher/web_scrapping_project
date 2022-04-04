from __future__ import print_function
from ctypes import sizeof
from re import sub
from types import NoneType
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from numpy import size
import requests
import csv

for  page_number in range(1, 38):
    # open url of website
    print('Scrapping Page: ' + str(page_number))
    url = 'https://www.stfrancismedicalcenter.com/find-a-provider/'
    body = {'PhysicianSearch$FTR01$PagingID': page_number}
    page_data_request = requests.post(url, data = body)
    # urlPage=urlopen(page_data_request).read()

    # using BeautifulSoup to parse data
    soup = BeautifulSoup(page_data_request.text, "html.parser")

    # create an array
    doctorData=[]

    # find link of  doctors profile
    for link in soup.find_all('a', class_ = "flex-top-between-block-500"):
        url_ = "https://www.stfrancismedicalcenter.com"+link.get('href')
        #print(url_)


        #create a dict
        docData={}
        #print("https://www.stfrancismedicalcenter.com"+link.get('href'))

        # find doctors name using link of profile
        profilePage= urlopen("https://www.stfrancismedicalcenter.com"+link.get('href')).read()
        soup = BeautifulSoup(profilePage, "html.parser")
        doctorName = soup.find('h1', class_ = "hide-1024")
        DoctorName= doctorName.text
        # print("Getting Doctor Name: "+DoctorName)



        #FIND Primary speciality
        doctorPrimarySpecialist = soup.find('li', class_ = "full flex-between-spaced-middle-wrap-block-550 mar-b-tiny ui-repeater")
        primarySpeciality = ""
        if(doctorPrimarySpecialist != None):
            specialityTag = doctorPrimarySpecialist.find('a')
            if(specialityTag != None):
                primarySpeciality= specialityTag.text
        
        
        #print("Speciality:" + primarySpeciality)


        #Find additional speciality
        doctorAdditionalSpecialist = soup.find('li', class_ = "flex-between-spaced-middle-wrap-block-550 mar-b-tiny ui-repeater")
        additionSpeciality = ""
        if(doctorAdditionalSpecialist != None):
            additionSpecialityTag = doctorAdditionalSpecialist.find('a')
            additionSpeciality = additionSpecialityTag.text
        
        #print("Add_Speciality:" +additionSpeciality)

        
        # Get contact number
        phone= soup.find('li', class_ = "half mar-e-tiny")
        phoneTag = phone.find('a')
        Phone= phoneTag.text
        #print("phone:" + Phone)
    

        #find address of doctors
        address = soup.find('li', class_ = "half mar-e-tiny")
        addressTag= address.find('address')
        AT= addressTag.contents
        city = ""
        # print(AT)
        if(AT != None and len(AT) > 2):
            city = AT[2].split(',')[0]


        AT= addressTag.text
        addressWithoutSlash = AT.replace('\n\t\t\t\t',"")
        addressWithoutPhone = addressWithoutSlash.replace(Phone, "")
        # print("Address without phone: "+addressWithoutPhone)
        #print("Address: "+AT)
        addresslineSplit= AT.splitlines()
        addressSplit = addresslineSplit[0].split(",")
        stateAndZip = addressSplit[len(addressSplit)-1].split()
        state = stateAndZip[0]
        #print("State: "+ State)
        zip= ""
        if (len(stateAndZip) > 1):
            zip = addressSplit[len(addressSplit)-1].split()[1]
        #print("Zip: "+ Zip)
        # print(addressTag.text)
        
    
        # find practise of doctors
        practiceTag= soup.find('strong', class_ = "title-style-5")
        practice=""
        if (practiceTag != None):
            practice= practiceTag.text
        #print(Practice)
        


        # dump data into json
        docData['URL']= url_
        docData['Full_Name']= DoctorName
        docData['Specialty']= primarySpeciality
        docData['Add_Specialty']= additionSpeciality
        docData['Full_Address']= addressWithoutPhone
        docData['City']= city
        docData['State']= state
        docData['Zip']= zip
        docData['Practice']= practice
        docData['Phone']= Phone
        doctorData.append(docData)
        #print(doctorData)

    jsonstr= json.dumps(doctorData)
    print('Saving File: ' + str(page_number))
    with open('/Users/poonamdhankher/Downloads/test/web_scrapping/docData' + str(page_number) + '.json', 'w') as f:
        print(jsonstr, file=f)




       

    
    