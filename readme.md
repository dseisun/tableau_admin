# Tableau Admin Scripts

This is a collection of scripts for features missing from the Tableau Admin suite of tools. It's focused on 

- archiving unused reports
- emailing extract owners of failed extracts
- parsing Tableau Desktop logs for queries
- exporting workbooks and datasources in XML without attached data
- Subscription framework that allows for more flexible report subscriptions

For all of this, a huge thanks to Ryan Mason for going through my crappy code, improving it everywhere, and writing 95% of the documentation

## Initial setup

Access our helper functions.

    export PYTHONPATH=CHECKOUT_DIR/libraries/

    export PYTHONPATH=$(pwd)/libraries/

## Dependencies

### virtual environments

Setup `virtualenv` to handle libraries.

http://docs.python-guide.org/en/latest/dev/virtualenvs/

### Postgres

Tableau Server is backed by a [Postgres](http://www.postgresql.org/) server. In order to be able to get information about the state of your server, the library requires that you have Postgres drivers installed. You'll also need to have a user that can access the system tables. Read this thread for an idea of how to go about this: http://community.tableau.com/message/340714#340714

Python Postgres Driver Downloads:
	- Windows: http://www.stickpeople.com/projects/python/win-psycopg/
	- OS X: [Homebrew](http://brew.sh/), `brew install postgres`
	- Ubuntu: sudo apt-get install python-psycopg2

### tabcmd

If you'd like to take actions on the server, you'll need a local copy of `tabcmd` to interact with the Tableau Server. 
To get tabcmd for mac/linux it's now pretty trivial on 9.0. Take a look at this post: http://community.tableau.com/message/343118#343118

### Catching emails in development

If you'd like to see the emails that these scripts send, try using [Mailcatcher](http://mailcatcher.me/) or a similar tool. Mailcatcher will act as an SMTP acceptor and will show you the messages in a browser. This is a great way to see what you're going to send before sending to everyone.

## Settings

All settings for these scripts live in `libraries/settings.py`. This file has constants used throughout these scripts. Not every setting is used by every script.

We recommend against checking this file in. We have included `libraries/settings.default.py` for reference. You can use it as a starting point for your settings with `$ cp libraries/settings.default.py libraries/settings.py`.

## Running

Each script can be run separately. They share a common set of libraries and settings in the `libraries/` folder.

### archive_unused_reports

Find all the reports that are longer than `settings.ARCHIVE_WINDOW`. Alert owners, delete them.

        $ python archive_unused_reports.py

### extract_error_email

Find all extracts from the last `settings.EXTRACT_ERROR_WINDOW_HOURS` hours. Email the owners the error messages.

        $ python extract_error_email.py

### client_log_parsing

Find queries in Tableau Desktop logs.

### tableau_export_workbooks

Export only the XML from Tableau Workbooks and data sources, and tries to insert the datasources into a database. Currently set up for Vertica. Needs to be abstracted for more export options

        $ python tableau_export_datascources.py

# subscriptions

This is a full framework for emailing reports to users. Some of the features:
	- Email multiple users
	- Each email may contain multiple dashboards from multiple different workbooks
	- (Slightly) intelligent caching. If a report is going to many users, it only pulls it down once.
	- Filtered subscriptions. This solves for: User A is only supposed to see data for California, and User B data for Wisconsin
	- Dynamic Filters (Sort of). Ex: Report can always be filtered to show only last saturday's data.

This is complex enough that it has its own readme in the subscriptions directory (readme.txt)

##queries

Collection of queries against the tableau postgres database that have been found to be useful.

## Tableau Server REST API

You can interact with the Tableau Server via the Rest API

http://onlinehelp.tableau.com/v8.2/server/en-us/help.htm#rest_api_ref.htm

Python example REST

http://onlinehelp.tableau.com/samples/en-us/rest_api/example.py
