#-------------------------------------------------------------------------------
# This file will get all statistics data(Including profile info) for all active players in 2011-2012. It can also fetch corresponding player list.
#-------------------------------------------------------------------------------

import re
import urllib
import time
import csv

urllist = ['0','100','200','300']
PlayerStats = open('Player_list.csv','w')
targeturl = "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=totals&per_minute_base=36&lg_id=NBA&is_playoffs=N&year_min=2012&year_max=2012&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&height_min=0&height_max=99&birth_country_is=Y&birth_country=&is_active=Y&is_hof=&is_as=&as_comp=gt&as_val=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&c5stat=&c5comp=gt&c6mult=1.0&c6stat=&order_by=ws&order_by_asc=&offset="
PlayerSalary = open('salary.csv','w')
OtherPlayerStats = open('Other_Stats.csv','w')
for i in urllist:
    finalurl = targeturl + i
    urlHandle = urllib.urlopen(finalurl)
    content = urlHandle.read()
    j = 0
    #fetches all values on search page
    pattern1 = re.compile('<td align(.*?)>(.*?)</td>')

    for match in pattern1.finditer(content):
        temp = match.group(2)
        pattern2 = re.search('<a href=".*?>(.*?)</a>',temp)
        # If the fetched data contains URL, then navigate URL page
        if pattern2 is not None:
            # writing player stats to file
            PlayerStats.write(pattern2.group(1)+",")
            #Navigate to corresponding player details page
            pattern3 = re.search('<a href=\"(\/players\/\w{1}\/\w+\d{2}\.html)\">([^<]*)</a>',temp)
            if pattern3 is not None:
                baseurl = "http://www.basketball-reference.com"
                #Form a new URL with the help of Player's given url and go to player details page
                newurl = baseurl + pattern3.group(1)
                newurlHandle = urllib.urlopen(newurl)
                newcontent = newurlHandle.read()
                #Find height
                Heightpattern = re.search('<span class="bold_text">Height:</span>(.*?)<span',newcontent)
                #Find Weight
                Weightpattern = re.search('<span class="bold_text">Weight:</span>(.*?)\n<br>',newcontent)
                #Find Experience
                Exppattern = re.search('<span class="bold_text">Experience:</span>(.*?)<',newcontent)
                #Find Name
                Namepattern = re.search('<h1>(.*?)</h1>',newcontent)
                #Find pattern for matching salary in 2011-12
                MatchingSalary = re.compile('<td align="left" >(\d{4}\-\d{2})</td>\n(.*?)csk=\"(\d{5,10})([^\"]*)(.*?)</tr>',re.DOTALL)
                for newmatchSalary in MatchingSalary.finditer(newcontent):
                    temp = newmatchSalary.group(2)
                    #finding team name
                    TeanName = re.search('<a href=\"(\/teams(.*?)\.html)\">([^<]*)</a>',temp)
                    # Writing player salary details to file
                    PlayerSalary.write(Namepattern.group(1)+","+newmatchSalary.group(1)+","+newmatchSalary.group(3)+","+TeanName.group(3)+"\n")
                #Find Position pattern in 2011-2012
                MatchingPosition = re.compile('<tr  class="full_table" id="per_game.2012">(.*?)<td align="center" >(.*?)</td>',re.DOTALL)
                for matchPosition in MatchingPosition.finditer(newcontent):
                #Write all player stats in file
                    OtherPlayerStats.write(Heightpattern.group(1)+","+Weightpattern .group(1)+","+Namepattern .group(1)+","+matchPosition.group(2)+","+Exppattern.group(1)+"\n")
        #If data is not URL, then simply write that to file
        else:
            PlayerStats.write(match.group(2)+",")
        j+=1
        if j == 31:
            PlayerStats.write("\n")
            j=0
    time.sleep(1)
PlayerStats.close()

