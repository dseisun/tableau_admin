from Subscription import Subscription
from TabEmail import TabEmail
from email.mime.text import MIMEText
import sys
sys.path.append('../libraries/')
from settings import TABLEAU_HOST, TABLEAU_SUBSCRIPTION_USER, TABLEAU_SUBSCRIPTION_PASSWORD, \
    SMTP_HOST, SMTP_PORT, SMTP_SSL, SMTP_USERNAME, SMTP_PASSWORD, TABCMD_PATH
from helper_functions import url_to_file_name, path_concat
from random import random
from time import sleep

import os
import argparse
import subprocess
import smtplib
import email
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime



parser = argparse.ArgumentParser(description='Daniel Seisun Subscription Script')
parser.add_argument('--config', action="store", dest="config",required=True, help="Path to the config XML file")
parser.add_argument('--to_override', action="store", dest="to_override", help="Override the destination of the email")
parser.add_argument('--file_override', action="store", dest="file_override", help="Override the filename parameter (Used to potentially point to a custom file). Must be used in conjuction with --skip_tabcmd")
parser.add_argument('--skip_tabcmd',  action='store_true', dest='skip_tabcmd', help="Override the saved_filename of the file")
parser.add_argument('--take_top', action="store", dest="take_top",type=int, help="Takes the top X rows of your list file")
parser.add_argument('--preprocess_script', action="store", dest="preprocess_script", help="Python script for preprocessing. Intended for dynamically creating distribution lists")
parser.add_argument('--avoid_ratelimits',  action='store_true', dest='avoid_ratelimits', help="Stagger the sending of emails to try to avoid being rate limited by gmail")
parser.add_argument('--skip_email', action='store_true', dest='skip_email', help='Set to skip sending the emails (useful if you just want the files downloaded)')
args = parser.parse_args()

config_xml = ET.parse(open(args.config, 'r'))

server = TABLEAU_HOST
username = TABLEAU_SUBSCRIPTION_USER
password = TABLEAU_SUBSCRIPTION_PASSWORD
tabcmd = TABCMD_PATH
save_path = config_xml.find('save_path').text
archive_path = config_xml.find('archive_path').text
smtp_server = SMTP_HOST
smtp_server_port = SMTP_PORT
mail_username = SMTP_USERNAME
mail_password = SMTP_PASSWORD
message_from = config_xml.find('message/from').text
message_subject = config_xml.find('message/subject').text
message_body = config_xml.find('message/body').text
csvpath = config_xml.find('csvfile').text

# Checking if there's a static attachment for the email
static_attach = ''
if len(config_xml.findall('static_attach')) == 1:
    static_attach = config_xml.find('static_attach').text

# Checking if the tableau_site parameter is defined. Otherwise falls back on default.
site = 'default'
if len(config_xml.findall('tableau_site')) == 1:
    site = config_xml.find('tableau_site').text

if args.preprocess_script:
    subprocess.call(['python', args.preprocess_script])

if args.take_top:
    take_top = args.take_top
else:
    take_top = 99999
sub = Subscription(csvpath, take_top)


# Actually creating the files
################################################################
if not(args.skip_tabcmd):
    if site == 'default':
        subprocess.call([tabcmd, 'login', '-s', server, '-u', username, '-p', password, '--no-prompt', '--no-certcheck'])
    else:
        subprocess.call([tabcmd, 'login', '-s', server,'-t', site, '-u', username, '-p', password, '--no-prompt', '--no-certcheck'])

    for row in sub.sub_rows:
        absolute_save_path = path_concat(save_path, url_to_file_name(row.url()))
        if not(os.path.isfile(absolute_save_path)):
            res = 1
            while res == 1:
                res = subprocess.call([tabcmd, 'export', row.url(), '-f', absolute_save_path, '--png', '--pagesize', 'unspecified', '--width', '1200', '--height', '800', '--timeout', '300', '--no-certcheck'])

        row.saved_path = absolute_save_path
# ################################################################

#Sending Emails
################################################################
if not (args.skip_email):
    if SMTP_SSL:
        smtp_conn = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
        smtp_conn.login(SMTP_USERNAME, SMTP_PASSWORD)
    else:
        smtp_conn = smtplib.SMTP(smtp_server, smtp_server_port)

    for email in sub.unique_emails():
        # Overrides
        ################################################################
        if args.file_override:
            filenames = [args.file_override]
        else:
            filenames = [email_row.saved_path for email_row in filter(lambda sub_row: sub_row.csv_dict['Email'] == email, sub.sub_rows)]

        if args.to_override:
            message_to = args.to_override
        else:
            message_to = email
        ################################################################
        msg = TabEmail(
            email_to=message_to,
            email_from=message_from,
            email_subject=message_subject,
            email_body=message_body,
            email_attachments_png=filenames,
            email_attachment_pdf=static_attach)
        smtp_conn.sendmail(message_from, message_to, msg.as_string())
        if args.avoid_ratelimits:
            sleep(random()*3)
##################################################################

# #Archiving Subscriptions
################################################################
if not(args.skip_tabcmd):
    directory = str(datetime.today().year) + "_" + str(datetime.today().month) + "_" + str(datetime.today().day)
    archive_dir = path_concat(archive_path, directory)
    if not (os.path.isdir(archive_path)):
        os.mkdir(archive_path)

    if not(os.path.isdir(archive_dir)):
        os.mkdir(archive_dir)
    for saved_file in {x.saved_path for x in sub.sub_rows}:
        shutil.copy(saved_file, archive_dir)
        os.remove(saved_file)
################################################################
