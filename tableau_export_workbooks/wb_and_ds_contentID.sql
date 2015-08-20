select 'Datasource' as SourceType, ds.repository_url, rd.content from datasources ds
inner join public.repository_data rd on rd.id = coalesce(ds.repository_data_id, ds.repository_extract_data_id)
union
select 'Workbook' as SourceType, wb.repository_url, rd.content from workbooks wb
inner join public.repository_data rd on rd.id = coalesce(wb.repository_data_id, wb.repository_extract_data_id)
