#Write Decorator for __init__ class?
import os
import xml.etree.ElementTree as ET

class TableauXML:
  def __init__(self, twb_file):
    self.twb_tree = ET.parse(twb_file)

  def get_datasource_info(self, datasource):
    """
    Returns a dict of most common available connection info.
    'relation_datasource' is the actual datasource when possible. If they use the tableau
    join dialogue, it's just a list of the tables in use.
    You can pass it a tableau workbook connection or a tds connection
    """
    connection = datasource.find('connection')
    datasource_info = {}
    datasource_info['class'] = connection.get('class')
    datasource_info['dbname'] = connection.get('dbname')
    datasource_info['server'] = connection.get('server')
    datasource_info['ds_name'] = datasource.find('repository-location').get('id')
    relation = datasource.find('connection/relation')

    rel_con_type = self.find_datasource_type(datasource)
    if rel_con_type == 'table':
      datasource_info['relation_datasource'] = relation.get('table')
    elif rel_con_type == 'text':
      datasource_info['relation_datasource'] = relation.text
    elif rel_con_type == 'join':
      join_tables = []
      for rel in relation.findall('.//relation'):
        if rel.get('table'):
          join_tables.append(rel.get('table'))
        datasource_info['relation_datasource'] = '\n'.join(join_tables)
    elif rel_con_type == 'tableau_connection':
      datasource_info['relation_datasource'] = datasource_info['dbname']
    return datasource_info

  def find_datasource_type(self, datasource):
    connection = datasource.find('connection')
    relation = connection.find('relation')
    if relation.get('type') == 'table' and relation.get('table') == '[sqlproxy]':
      return 'tableau_connection'
    elif relation.get('type') == 'table':
      return 'table'
    elif relation.get('type') == 'join':
      return 'join'
    elif relation.get('type') == 'text':
      return 'text'

class TableauWorkbook(TableauXML):
  """
  Series of helper functions for parsing tableau workbook XML
  """

  def __init__(self, twb_file):
    self.xml_tree = ET.parse(twb_file)
    self.connections = self.xml_tree.findall('./datasources/datasource/connection')
    self.datasources = self.xml_tree.findall('./datasources/datasource')
    self.wb_name = self.xml_tree.find('./repository-location').get('id')


class TableauDatasource(TableauXML):
  def __init__(self, tds_file):
    self.xml_tree = ET.parse(tds_file)
    self.connection = self.xml_tree.find('connection')
    self.datasource = self.xml_tree.getroot()

