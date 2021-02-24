import argparse
import urllib.request
import csv
import sys
import re
import operator
from datetime import datetime
from datetime import time

# SetUp Argument Parser - script requires a first position argument of a URL
parser = argparse.ArgumentParser()
parser.add_argument("URL")
link = parser.parse_args()
print("\n\tDownloading data from: " + (link.URL))
strurl = (link.URL)

# Method to download and decode the data into UTF-8
def downloadData(url):
    req = urllib.request.urlopen(url)
    decoded = str(req.read().decode('utf-8'))
    decodedList = decoded.split("\n")
    return decodedList

# Runs the above method to get the data from the URL passed in by the user.
# Input for this assignment: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
# DATA: path to file, datetime accessed, browser, status of request, request size in bytes

webData = downloadData(strurl)

# Read the data into a dictionary
csv_reader = csv.DictReader(webData)

row_count = 0
image_count = 0
browser_count = 0
firefox_count = 0
chrome_count = 0
ie_count = 0
safari_count = 0

# Regular Expression Searches
regexpImage = re.compile(r'.PNG|.JPG|.GIF|.png|.jpg|.gif')
regexpBrowser = re.compile(r'Firefox|Chrome|Internet Explorer|Safari')
regexpHours = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}')

for row in csv_reader:
    row_count += 1

    rowList = list(row.items())

    for x in rowList:
        xList = list(x)
        if regexpImage.search(xList[1]):
            #print("FOUND IMAGE: " + xList[1])
            image_count += 1
        elif regexpBrowser.search(xList[1]):
            #print("FOUND BROWSER: " +xList[1])
            browser_count += 1
            if "Firefox" in xList[1]:
                #print("FOUND FIREFOX: ", xList[1])
                firefox_count += 1
            elif "Chrome" in xList[1]:
                #print("FOUND CHROME: ", xList[1])
                chrome_count += 1
            elif "Internet Explorer" in xList[1]:
                #print("FOUND IE: ", xList[1])
                ie_count += 1
            elif "Safari" in xList[1]:
                #print("FOUND SAFARI: ", xList[1])
                safari_count += 1
        elif regexpHours.search(xList[1]):
            #print("FOUND HOURS: " + xList[1])
            splitXlist = xList[1].split(' ')
            timeList = splitXlist[1].split(':')
            hr = int(timeList[0])
            min = int(timeList[1])
            sec = int(timeList[2])

# Failed attempt at using datetime here ...
            rowTime = time(hr, min, sec)
            #print("hour =", rowTime.hour)
            #print("minute =", rowTime.minute)
            #print("second =", rowTime.second)

image_percentage = '{0:.2f}'.format((image_count / row_count * 100))
imageStr = (str(image_percentage) + '%')
print("\n\tImages account for", imageStr, "of all requests today")
print("\t\t ... there were", image_count, "images found out of", row_count, "rows of data")

#print("BROWSERS: ", browser_count)
#print("FIREFOX: ", firefox_count)
#print("CHROME: ", chrome_count)
#print("IE: ", ie_count)
#print("SAFARI: ", safari_count)

browserStats = {"Firefox":firefox_count, "Chrome":chrome_count, "Internet Explorer":ie_count, "Safari":safari_count}
print("\n\t", max(browserStats.items(), key=operator.itemgetter(1))[0], "had the highest amount of usage among browsers today")
mostKeyStr = str(max(browserStats.items(), key=operator.itemgetter(1))[0])
mostValueStr = mostKeyStr.strip()
print("\t\t...it was used", browserStats[mostValueStr], "times")