import itertools
import json
import sys

logFile = open(sys.argv[1], 'r')
outfile = open('./outfile.txt', 'w')
logElements = []
for line in logFile:
    logElements.append(json.loads(line))

logElementskSorted = sorted(logElements, key=lambda x: x['k'])

groupedLogElements = itertools.groupby(logElements, lambda x: x['k'])

queryInfo = []
for elem in logElements:
    if elem.get('k') == 'end-query':
        queryData = elem.get('v')
        queryData.update({'QueryEndTime': elem['ts']})
        queryInfo.append(queryData)

for query in queryInfo:
  outfile.write('------------------------------\n')
  outfile.write('%s: Query run in %s\n' % (query['QueryEndTime'],query['elapsed']))
  outfile.write('------------------------------\n')
  outfile.write(query['query'] + '\n')

# for line in groupedLogElements:
#   outfile.write(line[0] + '\n')
#   for group in line[1]:
#     outfile.write(str(group) + '\n')


# All json objects have
# k: Task name,
# k -> end-query
# v {query, rows, procoll, cols, elapsed}
# pid: ProcessID,
# req:  Not set in normal log,
# sess: Not set in normal log,
# sev,
# site: Not set in normal log,
# tid: Some sort of ID,
# ts: Timestamp,
# user,
# v: Task subdata
