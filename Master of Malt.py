from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import re
import time


url = "http://www.masterofmalt.com/country/scotch-whisky/"
baseurl = "http://www.masterofmalt.com"
webpage = urlopen(url)
soup = BeautifulSoup(webpage)

masterOfMaltReview = open('masterofmaltReview_part2.csv', 'w')

listing = soup.find('ul',{"title":"Distilleries links"})

try:
    aa = listing.findAllNext('li')
    for i in aa:
        distilleryname = i.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").encode('utf-8','ignore')

        ##Find All Href links in home page for all distillery
        newurl = i.find('a',href=True)
        if newurl:
            url1 = newurl.get('href')
            childurl = baseurl+url1
            childpage = urlopen(childurl)
            childsoup = BeautifulSoup(childpage)

            ##Find all review links in each distillery page
            anotherListing = childsoup.findAll('div',{"class":"boxBgr productBoxWide"})
            for each in anotherListing:
                newurl1 = each.find('a',href=True)
                if newurl1:
                    grandchildurl = newurl1.get('href')

            ## Get details from each page
                    grandchildpage = urlopen(grandchildurl)
                    grandchildsoup = BeautifulSoup(grandchildpage)
                    details1 = grandchildsoup.find('div',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl02_whiskyDetailsWrapper"})
                    details2 = grandchildsoup.find('div',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_whiskyDetailsWrapper"})

            ## Get all details
                    details = ""
                    if details1:
                        temp = details1.findAll('div',{"class":"whiskyDetails"})
                        for eachdetails in temp:
                            details = details + eachdetails.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore') + ";"
                    elif details2:
                        temp = details2.findAll('div',{"class":"whiskyDetails"})
                        for eachdetails2 in temp:
                            details = details + eachdetails2.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore') + ";"
                    else:
                        print grandchildurl
                        print "No match"
            ## Get Title
                    titleFind = grandchildsoup.find('h1',{"itemprop":"name"})
                    if titleFind:
                        title = titleFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore')
                    else:
                        title = "None"

            ## Get price
                    priceFind = grandchildsoup.find('span',{"itemprop":"price"})
                    if priceFind:
                        price = priceFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").encode('utf-8','ignore')
                    else:
                        price = "None"

            ## Get ratings
                    ratingFind = grandchildsoup.find('div',{"class":"productUserRating"})
                    if ratingFind:
                        zz = ratingFind.findNext('div')
                        rating = zz.get('title').strip('\n\r\t').replace("\n"," ").replace("\t"," ").encode('utf-8','ignore')
                    else:
                        rating = "0"

            ## Get tasting notes
                    notes = grandchildsoup.find('div',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_tastingNoteWrap"})
                    if notes:
                        noseFind = notes.find('p',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_noseTastingNote"})
                        palateFind = notes.find('p',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_palateTastingNote"})
                        finishFind = notes.find('p',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_finishTastingNote"})
                        overallFind = notes.find('p',{"id":"ctl00_ContentPlaceHolder1_ctl01_ctl01_overallTastingNote"})
                        if noseFind:
                            nose = noseFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore')
                        else:
                            nose ="None"
                        if palateFind:
                            palate = palateFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore')
                        else:
                            palate ="None"
                        if finishFind:
                            finish = finishFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore')
                        else:
                            finish ="None"
                        if overallFind:
                            overall = overallFind.get_text().strip('\n\r\t').replace("\n"," ").replace("\t"," ").replace(","," ").encode('utf-8','ignore')
                        else:
                            overall ="None"

                    else:
                        nose ="None"
                        palate ="None"
                        finish ="None"
                        overall ="None"

                    masterOfMaltReview.write(distilleryname+","+title+","+ details+price+","+rating+","+nose+","+palate+","+finish+","+overall+"\n")
                    time.sleep(1)
               #     print distilleryname+","+title+","+ details+","+price+","+rating+","+nose+","+palate+","+finish+","+overall+"\n"
except:
    pass
masterOfMaltReview.close()