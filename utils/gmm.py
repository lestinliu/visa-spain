import datetime
import imaplib, email
import quopri
import re


class Email:

    def make_seen(self, username, password):
        mail = imaplib.IMAP4_SSL('imap.{}'.format(username.split("@")[1]))
        mail.login(username, password)
        mail.list()
        mail.select('inbox')
        result, data = mail.uid('search', None, "UNSEEN")  # (ALL/UNSEEN)
        i = len(data[0].split())  # emails count
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            mail.uid('fetch', latest_email_uid, '(RFC822)')

    def read_email(self, username, password):
        mail = imaplib.IMAP4_SSL('imap.{}'.format(username.split("@")[1]))
        mail.login(username, password)
        mail.list()
        mail.select('inbox')
        result, data = mail.uid('search', None, "UNSEEN")  # (ALL/UNSEEN)
        i = len(data[0].split())  # emails count
        found = ""
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email_string = email_data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            # Header Details
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            # Body details
            if subject == "Email verification":
                for part in email_message.walk():
                    print(subject)
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        m = re.search('Verification code - (.+?)<br', body.decode('utf-8'))
                        found = m.group(1)
                        break
                    else:
                        continue
                break
        print("found: ", found)
        return found
