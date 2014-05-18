#-------------------------------------------------------------------------------
# Name:        module1
# This file will get the list of all players with their basic details of all active players between 2001-2014 
#-------------------------------------------------------------------------------

import re
import urllib
import time
import csv

out = open('Player_2001_2014_regex.csv','w')
targeturl = "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=totals&per_minute_base=36&lg_id=NBA&is_playoffs=N&year_min=2002&year_max=2014&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&height_min=0&height_max=99&birth_country_is=Y&birth_country=&is_active=Y&is_hof=&is_as=&as_comp=gt&as_val=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&c5stat=&c5comp=gt&c6mult=1.0&c6stat=&order_by=ws&order_by_asc=&offset="

for PageNo in range(0,3200,100):
    finalurl = targeturl + str(PageNo)
    urlHandle = urllib.urlopen(finalurl)
    content = urlHandle.read()
    count = 0
    #fetches all values on search page
    pattern1 = re.compile('<td align(.*?)>(.*?)</td>')

    for match in pattern1.finditer(content):
        temp = match.group(2)
        pattern2 = re.search('<a href=".*?>(.*?)</a>',temp)
        if pattern2 is not None:
            out.write(pattern2.group(1)+",")
        else:
            out.write(match.group(2)+",")
        count+=1
        if count == 31:
            out.write("\n")
            count=0
        time.sleep(1)
out.close()
