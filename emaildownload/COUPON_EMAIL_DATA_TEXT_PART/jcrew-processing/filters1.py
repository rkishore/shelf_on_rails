import os
import re

USERNAME = "rootofsavvypurse"

DST_LOCATION = "./COUPON_EMAIL_DATA_TEXT_PART/" + USERNAME

DATE = "17Dec2011"
FILENAME = DST_LOCATION + "/" + DATE  + "/18_37_14_J.Crew"

# regular expression to catch: December 18, 2011 OR Dec, 18, 2011 OR Dec 18 2011
DATE_PATTERN = "[a-zA-Z,]+ [\d,]+ [\d]+"

# regular expression to catch: 12/21 or 12.21
DATE_PATTERN2 = "[\d]+[\/.][\d]+"

date_reg_ex = re.compile(DATE_PATTERN)
date_reg_ex2 = re.compile(DATE_PATTERN2)


months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


# commonly used keywords to check how long the coupon is valid
validity_keywords = ["THROUGH", "LIMITED TIME", "ENDS SOON", 
                     "TODAY ONLY", "LAST DAY", "THROUGH TONIGHT"]

# check if it's available in
# a. only in stores
# b. only online
# c. both
availability_keywords = ["IN STORES & ONLINE", "IN STORES ONLY", "ONLINE ONLY", 
                         "IN-STORE", "IN STORES AND ONLINE"]


shipping_keywords = ["DAYS LEFT", "SHIP", "ORDER BY"]

LINES = ""

END_LINE_MARKER = "."
START_LINE_MARKER = "\n"

def find_lines_containing_keyword(keyword):
    result_list = []
    count = LINES.count(keyword)
    start = 0
    last_start = 0
    #same keyword may appear multiple times in the file
    for j in range(0, count):
        start = LINES.find(keyword, start+1)
        if start > 0:
            END_OF_LINE = LINES.find(END_LINE_MARKER, start)
            BEGIN_OF_LINE = LINES.rfind(START_LINE_MARKER, last_start, start)
            result = LINES[BEGIN_OF_LINE+1: END_OF_LINE+1]
            #print "Keyword: [" + keyword + "] " + result
            result_list.append(result)
            last_start = start
    return result_list
                
            
def process_availability():
    for i in range(0, len(availability_keywords)):
        keyword = availability_keywords[i]
        result_list = find_lines_containing_keyword(keyword)
        if len(result_list) > 0:
            print keyword, result_list
            return keyword
    
def find_date(line):
    for j in range(0, len(line)):
        for i in range(0, len(months)):
            count = line[j].find(months[i])
            #print "Found " + months[i] + " in " + line[j] + " location: " + str(count)
            if count > 0:
                result = date_reg_ex.search(line[j])
                if (not (result == None)):
                    print result.group()
                    #return (1, result.group(0))
                else:
                    result = date_reg_ex2.search(line[j])
                    if (not (result == None)):
                        print result.group()
    return (0, "TODAY")    
        
def process_validity():
    for i in range(0, len(validity_keywords)):
        keyword = validity_keywords[i]
        result_list = find_lines_containing_keyword(keyword)
        if len(result_list) > 0:
            print keyword, result_list
            exists, date = find_date(result_list)
            if exists == 1:
                print date
                #return date
            #else:
                #return keyword

if __name__ == "__main__":
    
    for f in os.listdir(DST_LOCATION):
        f_path = DST_LOCATION + "/" + f
        if os.path.isdir(f_path):
            for infile in os.listdir(f_path):
    
                fp = open (f_path + "/" + infile)
                print "\n\nAnalyzing " + f_path + "/" + infile
                lines = ""
                
                for l in fp.readlines():
                    lines += l 
                    
                fp.close()    
            
                LINES = lines.upper()
                #print LINES
                
                print "VALIDITY = "  +  str(process_validity())
                
                print "AVAILABILITY = " + str(process_availability())