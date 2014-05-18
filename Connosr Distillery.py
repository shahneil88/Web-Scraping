from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import re
import time

baseurl = "http://www.connosr.com"
url = "http://www.connosr.com/whisky"
webpage = urlopen(url)
soup = BeautifulSoup(webpage)

connosrdistillery = open('ConnosrDistillery.csv', 'w')
distillerylist = soup.findAll('li',{"class":"bottle"})

for founddistillery in distillerylist:
    distilleryname = founddistillery.find("h3")
    name = distilleryname.get_text().strip('\n\t\r').replace(","," ")

    ## Navigating to Child Page for details of each whisky
    a_link = distilleryname.find('a', href = True)
    childurl = a_link.get('href')
    newurl = baseurl+childurl
    childpage = urlopen(newurl)
    childsoup = BeautifulSoup(childpage)
    profile = childsoup.find('div',{"class":"content-inner padding-vertical natural-height"})

    ## Get the Water Source details
    try:
        water_source_list = profile.findAll("li")
        water_sourceRegex = re.compile('Water Source:</span>(.*?)</li>',re.DOTALL)
        water_sourcePattern = water_sourceRegex.search(str(water_source_list))
        water_source = water_sourcePattern.group(1).strip('\n\r\t')
    except Exception as e:
        water_source = "None"

    ## Get the Address Details
    try:
        addressRegex = re.compile('Address:</span>(.*?)</li>',re.DOTALL)
        addressPattern = addressRegex.search(str(water_source_list))
        address = addressPattern.group(1).strip('\n\r\t').replace(',',' ')

    except Exception as e:
        address = "None"

    ## Get the tag list
    try:
        tags = ""
        taglist = childsoup.find('ul',{"class":"tag-list clearfix"})
        for tag in taglist.findAll('li'):
            tags += tag.get_text().strip('\n\t\r').replace(',',';')
    except:
        tags = "None"

    ## Getting Region data
    region = founddistillery.find('div',{"class":"browse-info-1"})
    regiontext = region.get_text().strip('\n\t\r')
    regexCompile = re.compile('Region: (.*?)Whiskie',re.DOTALL)
    regionPattern = regexCompile.search(regiontext)
    if regionPattern == None:
        region = "None"
    else:
        region = regionPattern.group(1).strip('\n\r\t').replace(","," ")

    ## Getting Review Data
    reviews = founddistillery.find('div',{"class":"browse-info-2"})
    reviewtext = reviews.get_text().strip('\n\t\r')
    regexCompile1 = re.compile('(\d+)',re.DOTALL)
    reviewPattern = regexCompile1.search(reviewtext)
    reviews = reviewPattern.group(1).strip('\n\r\t').replace(","," ")

    print name + "," + region + ","+ reviews+","+ water_source+","+address+","+tags
    ## Write to file
    connosrdistillery.write(name+","+region+","+reviews+","+ water_source+","+address+","+tags+"\n")
    time.sleep(1)
connosrdistillery.close()