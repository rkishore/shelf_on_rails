import email
import os, glob
import commands


from email.parser import Parser

USERNAME = "rootofsavvypurse"
SRC_LOCATION = "./COUPON_EMAIL_DATA/" + USERNAME

DST_LOCATION = "./COUPON_EMAIL_DATA_TEXT_PART/" + USERNAME

DATE = "17Dec2011"
FILENAME = SRC_LOCATION + "/" + DATE  + "/18_37_14_J.Crew"
#FILENAME = STORE_LOCATION + "/" + DATE + "/test.txt"

def process_file(src_filename, dst_filename):
    FILE = open(src_filename)
    msg = email.message_from_file(FILE)
    #print msg.as_string()
    print msg.keys()
    print msg.values()
    print msg['Subject']
    print msg['To']
    print msg['From']
    for part in msg.walk():
        # each part is a either non-multipart, or another multipart message
        # that contains further parts... Message is organized like a tree
        if part.get_content_type() == 'text/plain':
            print part.get_payload()
            FILE_OUTPUT = open(dst_filename, "w")
            FILE_OUTPUT.write(msg['From'] + "\n")
            FILE_OUTPUT.write(msg['To'] + "\n")
            FILE_OUTPUT.write(msg['Subject'] + "\n")
            FILE_OUTPUT.write(part.get_payload())
            FILE_OUTPUT.close()
        
def create_dir(dir_name):
    cmd = "mkdir -p " +  str(dir_name)
    print cmd
    print commands.getoutput(cmd)        
        
if __name__ == "__main__":     
    
    create_dir(DST_LOCATION)
    # We iterate through all subdirectories and the files inside them 
    # and process them
    print "Looking at " + SRC_LOCATION
    for f in os.listdir(SRC_LOCATION):
        f_path = SRC_LOCATION + "/" + f
        d_path = DST_LOCATION + "/" + f 
        print "Processing file " + f + " " + str(os.path.isdir(f_path))
        if os.path.isdir(f_path):
            create_dir(d_path)
            print "Yes, " + str(f_path) + " is a directory"
            for infile in os.listdir(f_path):
                print "Inside dir " + f_path + " processing file " + infile
                process_file(f_path + "/" + infile, d_path + "/" + infile)
        else:
            process_file(f_path, d_path)