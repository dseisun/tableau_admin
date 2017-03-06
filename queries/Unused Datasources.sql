select su.name || '@twitter.com' as owner, ds.name  from datasources ds
left join public.data_connections dc on dc.dbname = ds.repository_url and dc.owner_type = 'Workbook' and server = 'tableau.twitter.biz'
left join users u on u.id =  ds.owner_id 
left join system_users su on su.id = u.system_user_id
where dc.id is null