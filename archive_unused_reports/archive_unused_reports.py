#To be run on a windows machine with tabcmd in the path
from itertools import groupby
import psycopg2
import smtplib
import subprocess
import argparse
import os

################################################################################
# Local libraries
################################################################################
from helper_functions import list_dict, sendEmail, load_template,\
 tabcmd_installed, url_to_file_name, tableau_login
import settings

################################################################################
# Connnection
################################################################################
conn = psycopg2.connect(
  host     = settings.TABLEAU_HOST,
  port     = 8060,
  database = "workgroup",
  user     = settings.TABLEAU_POSTGRES_USER,
  password = settings.TABLEAU_POSTGRES_PASSWORD)

################################################################################
# Query or email template
################################################################################
query_template = load_template("archive_unused_reports.sql.template")

query = query_template.format(
  archive_window = settings.ARCHIVE_WINDOW,
  domain = settings.EMAIL_DOMAIN)

################################################################################
# Data to process
################################################################################
curs = conn.cursor()
curs.execute(query)
records = list_dict([col.name for col in curs.description], curs.fetchall())
email_sort = sorted(records, key = lambda rec: rec['owner_email'])
unique_emails = groupby(email_sort, lambda rec: rec['owner_email'])

################################################################################
# Emailing the report owners
################################################################################
with open("archive_unused_reports.html.template", "r") as f:
  body_template = f.read()

for line in unique_emails:
  email = line[0]
  workbooks = map(lambda rec: rec['workbook'], list(line[1]))
  subj = 'Archiving unused Tableau Reports'
  body = body_template.format(
    archive_window = settings.ARCHIVE_WINDOW,
    contact        = settings.CONTACT_NAME,
    workbook_list  = ',</li><br><li>'.join(workbooks))

  sendEmail(settings.CONTACT_EMAIL, email, subj, body, isHTML=True)

################################################################################
# Downloading and deleting Reports
################################################################################
if not tabcmd_installed():
  print "tabcmd not found"
  exit()

for report in sorted(records, key = lambda rec: rec['url_namespace']):
  tableau_login(settings.TABADMIN_USER, settings.TABADMIN_PASSWORD,
    report['url_namespace'])
  path_concat(settings.ARCHIVE_LOCATION, url_to_file_name(report['workbook'],'twb'))

  get_cmd = [
      'tabcmd', 'get', '/workbooks/{0}.twb'.format(report['repository_url']),
      '-f',report_uri,
      '--timeout', '600']
  print "Executing: {0}".format(subprocess.list2cmdline(get_cmd))
  if tabcmd_installed(): subprocess.call(get_cmd)

  if os.path.exists(report_uri):
    delete_cmd = ['tabcmd', 'delete',
      '--workbook', report['workbook'],
      '--project', report['project'],
      '--timeout', '600']
    print "Executing: {0}".format(subprocess.list2cmdline(delete_cmd))
    if tabcmd_installed(): subprocess.call(delete_cmd)
