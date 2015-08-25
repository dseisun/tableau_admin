import os

TABLEAU_HTTP = 'http://' #add an 's' if you're using SSL
TABLEAU_HOST = 'my_uber_cool_tableau_server.com'
TABLEAU_SUBSCRIPTION_USER = 'tableau_user_used_for_subscriptions'
TABLEAU_SUBSCRIPTION_PASSWORD = 'HiGithub!'
TABLEAU_POSTGRES_USER = 'dseisun'
TABLEAU_POSTGRES_PASSWORD = 'IllBetNoOneEverUsesThisAnyways'
TABADMIN_USER = None
TABADMIN_PASSWORD = None
ARCHIVE_WINDOW = 90
CONTACT_NAME = 'Daniel Seisun' #Used for error emails if workbook owner isn't found
CONTACT_HANDLE = 'dseisun' #Used for error emails if workbook owner isn't found
CONTACT_EMAIL = 'dseisun@twitter.com' #Used for error emails if workbook owner isn't found
CONTACT_NAME_ALTERNATE = 'PERSON 2' #Used for error emails if workbook owner isn't found
EMAIL_DOMAIN = 'twitter.com'
#Settings currently configured for gmail
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USERNAME = 'myemail@gmail.com'
SMTP_PASSWORD = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
SMTP_SSL = True
ARCHIVE_LOCATION = '/home/dseisun/tableau/report_archiving'
DEFAULT_CC = None
EXTRACT_ERROR_WINDOW_HOURS = 24
TABCMD_PATH = '/home/dseisun/tableau_rest_api/tabcmd/tabcmd.sh' #Supports OSX/Linux or Windows
