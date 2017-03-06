select workbook, repository_url, wb_created_at, project, wb_owner || '@twitter.com' as owner_email, wb_owner, url_namespace, max(event_created_at) as most_recent_view from (
select 
        
        proj.name as project,        
        wb.created_at as wb_created_at,
        he.created_at as event_created_at,
        hwb.name as workbook,
        wb.repository_url,
        now() at time zone 'utc' - he.created_at as time_since_action,
        sites.url_namespace,
        su.name as wb_owner
from historical_events he
left join historical_event_types het on het.type_id = he.historical_event_type_id
left join hist_users as hist_users_a on hist_users_a.id = he.hist_actor_user_id
left join hist_users as hist_users_t on hist_users_t.id = he.hist_target_user_id
left join hist_workbooks hwb on hwb.id = he.hist_workbook_id
left join hist_views hv on hv.id = he.hist_view_id
left join hist_sites s on s.id = he.hist_actor_site_id
left join sites on sites.id = s.site_id
left join (
        select max(workbook_id) as cur_id, name from hist_workbooks
        group by name) cur_wb on cur_wb.name = hwb.name
left join workbooks wb on wb.id = cur_wb.cur_id
left join projects proj on proj.id = wb.project_id
left join users u on u.id =  wb.owner_id 
left join system_users su on su.id = u.system_user_id
where het.name = 'Access View'
and wb.name is not null
and wb.created_at < (current_date - 60)) x 
group by x.workbook, x.repository_url, x.wb_created_at,x.project, x.wb_owner, x.url_namespace
--Haven't been used in last 60 days
having max(event_created_at) < (current_date - 60)
order by most_recent_view desc


