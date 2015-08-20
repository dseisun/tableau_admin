from itertools import groupby
import psycopg2
import smtplib
import helper_functions
from helper_functions import cleanDirPath
import subprocess
import argparse
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import xml
import sqlparse
from tableau_xml import TableauDatasource as TDS
from tableau_xml import TableauWorkbook as TWB
import csv
import vertica_python
import settings


parser = argparse.ArgumentParser(description='Daniel Seisun Archive old reports script')
parser.add_argument('--postgres_user', action="store", dest="postgres_user",required=True,  help="Postgres Username")
parser.add_argument('--postgres_pass', action="store", dest="postgres_pass", required=True,  help="Postgres Password")
parser.add_argument('--archive_path', action="store", dest="archive_path", required=True,  help="Where to store the workbook files")
parser.add_argument('--vert_user', action='store', dest='vert_user', required=False, help='Username to database to store workbook connection info')
parser.add_argument('--vert_pass', action='store', dest='vert_pass', required=False, help='Password to database to store workbook connection info')
args = parser.parse_args()



########################################
#Pulling down twb, twbx, tds, and tdsx files
########################################
conn = psycopg2.connect(host=settings.TABLEAU_HOST, port=8060,database="workgroup", user=args.postgres_user, password=args.postgres_pass)
print 'Pulling down twb and twbx files from server...'
twbx_workbooks_query = open('./wb_and_ds_contentID.sql', 'r').read()
curs = conn.cursor()
curs.execute(twbx_workbooks_query)
workbook_query_records = helper_functions.list_dict([col.name for col in curs.description], curs.fetchall())

def tabExport(record):
	if record['sourcetype'] == 'Datasource':
		fileExt = 'tdsxm'
		fileSearch = 'tds'
	elif record['sourcetype'] == 'Workbook':
		fileExt = 'twbxm'
		fileSearch = 'twb'
	lobj = psycopg2.extensions.lobject(conn, record['content'], 'r')
	file_path = '%s/%s.%s' % (args.archive_path, record['repository_url'], fileExt)
	lobj.export(file_path)
	if zipfile.is_zipfile(file_path):
		file_zip = zipfile.ZipFile(file_path)
		for files in file_zip.namelist():
			if files.find('.%s' % fileSearch) > 0:
				file_zip.extract(files, path=args.archive_path)
		os.remove(file_path)
	else:
		os.rename(file_path, file_path[:-2])

for record in workbook_query_records:
	tabExport(record)

########################################
#Loading files into vertica
########################################
print 'Parsing files and inserting to vertica...'
wb_table_name = "test.DSEISUN_tableau_wb_datasources"
tds_table_name = "test.DSEISUN_tableau_server_datasources"

vert_connection = vertica_python.connect({
   'host': '127.0.0.1',
   'port': 5436,
   'user': args.vert_user,
   'password': args.vert_pass,
   'database': 'analytics_raw'
   })


twb_files = (x for x in os.listdir(args.archive_path) if x[-3:] == 'twb')
tds_files = (x for x in os.listdir(args.archive_path) if x[-3:] == 'tds')
all_files = {'workbook': twb_files, 'tableau_datasource': tds_files}

vert_curs = vert_connection.cursor()
for twb_file in twb_files:
   print twb_file
   twb = TWB(open(cleanDirPath(args.archive_path) + twb_file, 'r'))
   for wb_con in twb.datasources:
      if twb.find_datasource_type(wb_con) <> 'param':
         conn_info = twb.get_wb_datasource(wb_con)
         row = (twb.wb_name, conn_info['ds_name'], conn_info['class'], conn_info['server'], conn_info['dbname'], conn_info['relation_datasource'].encode('ascii', errors='backslashreplace'))
         vert_curs.execute("insert into %s VALUES (:0|, :1|, :2|, :3|, :4|, :5|)" % wb_table_name, {'0|':row[0], '1|':row[1], '2|':row[2], '3|':row[3], '4|':row[4], '5|':row[5]})

for tds_file in tds_files:
   print tds_file
   tds = TDS(open(cleanDirPath(args.archive_path) + tds_file, 'r'))
   conn_info = tds.datasource_info
   row = (conn_info['ds_name'], conn_info['class'], conn_info['server'], conn_info['dbname'], conn_info['relation_datasource'].encode('ascii', errors='backslashreplace'))
   vert_curs.execute("insert into %s VALUES (:0|, :1|, :2|, :3|, :4|)" % tds_table_name, {'0|':row[0], '1|':row[1], '2|':row[2], '3|':row[3], '4|':row[4]})
print "Committing Files"
vert_curs.execute('commit;')
print "Complete!"