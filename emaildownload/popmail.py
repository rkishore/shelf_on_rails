import getpass
import poplib
import sys
import commands
import email


#USERNAME = "rootofspontalicious"
USERNAME = "rootofsavvypurse"
POPSERVER = "pop.gmail.com"

STORE_LOCATION = "./COUPON_EMAIL_DATA/" + USERNAME
# Importing emails from our gmail accounts

def connect():
    M = poplib.POP3_SSL(POPSERVER, port=995)
    #M.conn.sock.setblocking(0)
    M.user(USERNAME)
    M.pass_(getpass.getpass())
    numMessages = len(M.list()[1])
    print numMessages
    return M


def find_time_received(mail):
    #print mail
    words = mail.split()
    #print words
    loc = words.index("Date:")
    print "Time exists at loc " + str(loc)
    day1 = words[loc+1]
    
    # some emails have "date: wed, 8 dec 2011 time"
    # and others have "date: 8 dec 2011 time"
    index = 1
    if valid(day1):
        index = 0
    time = words[loc+index+4]
    print "TIME: " + time
    return time
    
def valid(day):
    try:
        y = int(day)
        return 1
    except ValueError:
        return 0
    
def find_date_received(mail):
    words = mail.split()
    print words
    loc = words.index("Date:")
    print "Date exists at loc " + str(loc)
    day1 = words[loc+1]
    
    # some emails have "date: wed, 8 dec 2011 time"
    # and others have "date: 8 dec 2011 time"
    index = 1
    if valid(day1):
        index = 0
    day = words[loc+index+1]
    mon = words[loc+index+2]
    year = words[loc+index+3]
    print "DAY: " + day + " " + " DAY1: " + day1 + " index: " + str(index)
    day_formatted = format_day(day)
    
    date = str(day_formatted) + "" + mon + "" + year
    print "DATE: " + date
    return date
    
    
def find_sender(mail):
    words = mail.split()
    loc = words.index("From:")
    sender = words[loc+1]
    print "SENDER: " + sender
    return sender
    
def format_day(day):
    if (int(day) < 10 and int(day) > 0):
        if (len(day) < 2):
            new_day = "0" + day
            return new_day
        
    return day    
    
def format_sender(sender_raw):
    s1 = sender_raw.replace('<', '')
    s2 = s1.replace('>', '')
    s3 = s2.replace('+', '')
    s4 = s3.replace('\"', '')
    s5 = s4.replace('\'', '')
    return s5
    
def store(mail):
    print "Storing email now" + str(mail)
    date_received = find_date_received(mail)
    time_received = find_time_received(mail)
    sender_raw = find_sender(mail)
    
    sender = format_sender(sender_raw)
    #return
    # create the directory for the date
    d = STORE_LOCATION + "/" + date_received
    createDir(str(d))
    
    time_received_new = time_received.replace(":", "_")
    filename = d + "/" + time_received_new + "_" + sender
    print "Creating file " + str(filename) + ".\n"
    
    
    result = commands.getoutput("touch " + str(filename))
    print " result = " + str(result)
    FILE = open(str(filename), 'r+')
    #FILE = open(str(d) + "/atul.txt", 'w')
    FILE.write(mail)
    #FILE.write("Hello!\n")
    FILE.close()
    
    
def process(mail):
    msg = email.message_from_string(mail)
    #print msg  
    #print msg.keys()
    #print msg['Subject']
    for part in msg.walk():
    # each part is a either non-multipart, or another multipart message
    # that contains further parts... Message is organized like a tree
        #if part.get_content_type() == 'text/plain':
        print part.get_payload()
    
def fetch(Handle):
    # store each email in a separate file
    # name of file:
    # directory: date when email was received
    numMessages = len(Handle.list()[1])
    for i in range(numMessages):
        #print str(Handle.retr(i+1))
        mail = ""
        for j in Handle.retr(i+1)[1]:
            #print str(i) + " " + j
            mail = mail + " " + str(j) + "\n"
            #msg = email.message_from_string(j)
            #print msg 
            #print "Item: " + str(j)
        mail += "\n"
        #print mail
        store(mail)
        #process(mail)
        #store(Handle.retr(i+1))

def createDir(dir_name):
    cmd = "mkdir -p " +  str(dir_name)
    print cmd
    print commands.getoutput(cmd)

if __name__ == "__main__":
    
    print STORE_LOCATION
    createDir(STORE_LOCATION)
    Handle = connect()
    fetch(Handle)