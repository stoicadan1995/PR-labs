import imaplib
import email
import smtplib
from email.mime.text import MIMEText

user_email = 'stoicaprlabs@gmail.com'
user_password = 'just4prlabs'

mail = imaplib.IMAP4_SSL('imap.gmail.com')

def connect_gmail_imap():
    global mail, gmail_connected
    mail.login(user_email, user_password)
    mail.select("INBOX")
    result2, new_messages = mail.search(None, '(UNSEEN)')
    gmail_connected = True
    print 
    print "LOGGED IN " + user_email
    print "New Messages : " + str(len(new_messages[0].split()))

def send_mail():
    global mail
    print
    print 'NEW MESSAGE'
    print 'MESSAGE'
    msg = MIMEText(raw_input())
    print 'SUBJECT'
    msg['Subject'] = raw_input()
    print 'EMAIL'
    to_email = raw_input()
    msg['To'] = to_email
    print 'CC:'
    msg['CC'] = raw_input()
    msg['From'] = user_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(user_email, user_password)
    server.sendmail(user_email, to_email, msg.as_string())
    server.quit()

def get_last_messages():
    global mail
    print 'Enter number of emails : '
    n = int(input())
    result, data = mail.uid('search', 'CHARSET', 'UTF-8', "ALL")
    listIDS = data[0].split()
    lastEMAIL = len(listIDS) - 1
    for i in range(n):
        currentMailID = listIDS[lastEMAIL - i]
        result2, message_fetch = mail.uid('fetch', currentMailID, '(RFC822)')
        raw_email = message_fetch[0][1]
        email_message = email.message_from_string(raw_email)
        print 
        print 'Subject: ' + email_message['subject']
        print 'Sender: ' + email_message['from']
        print 'Date: ' + email_message['Date']

        attachment_count = 0

        for part in email_message.walk():
            if part.get('Content-Disposition') is None:
                continue
            attachment_count += 1
        
        if attachment_count != 0:
            print str(attachment_count) + ' attachments found'

        if email_message.is_multipart():
            for part in email_message.get_payload():

                text = None
            
                if part.get_content_charset() is None:
                    text = part.get_payload(decode=True)
                    continue

                if part.get_content_type() == 'text/plain':
                    charset = part.get_content_charset()
                    text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                if text is not None:
                    print
                    print 'First sentence: ' + text.strip().split('\n')[0]
                    print

connect_gmail_imap()

get_last_messages()

send_mail()

print 'Goodbye'