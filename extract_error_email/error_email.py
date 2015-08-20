import psycopg2
from helper_functions import list_dict, sendEmail
import email
import smtplib
import argparse

################################################################################
# Local libraries
################################################################################
from helper_functions import load_template
import settings

################################################################################
# Connection
################################################################################
conn = psycopg2.connect(
  host     = settings.TABLEAU_HOST,
  port     = 8060,
  database = "workgroup",
  user     = settings.TABLEAU_USER,
  password = settings.TABLEAU_PASSWORD)

curs = conn.cursor()

################################################################################
# Template query
################################################################################
query_template = load_template("error_email.sql.template")
query = query_template.format(
  default_owner = settings.CONTACT_HANDLE,
  hour = settings.EXTRACT_ERROR_WINDOW_HOURS)

################################################################################
# Get query results
################################################################################
curs.execute(query)
records = list_dict([col.name for col in curs.description], curs.fetchall())

################################################################################
# Send emails
################################################################################
body_template = load_template("error_email.html.template")

for line in records:
  workbook_title = line['title']

  email_title = 'Action Required - Tableau Extracts Failing - {title}'\
    .format(title = workbook_title)

  body = body_template.format(
    workbook_title = workbook_title,
    fail_time      = line['time_since_failure_pst'],
    error_message  = line['notes'],
    contact        = settings.CONTACT_NAME,
    contact2       = settings.CONTACT_NAME_ALTERNATE)

  sendEmail(settings.CONTACT_EMAIL,
    line['wb_owner'] + '@' + settings.EMAIL_DOMAIN,
    email_title,
    body,
    True)
