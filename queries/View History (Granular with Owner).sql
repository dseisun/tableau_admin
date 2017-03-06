select 
        hist_users_a.name as action_username, 
        hist_users_t.name as target_username,
        he.hist_workbook_id,
        he.created_at,
        het.name as action, 
        hwb.name as workbook,
        hv.name as view,
        now() at time zone 'utc' - he.created_at as time_since_action,
        s.name as Site,
        su.name as wb_owner,
        hg.name as group_name,
        case when wb.name is null then 'Deleted' else 'Exists' end as wb_exists
        from historical_events he
left join historical_event_types het on het.type_id = he.historical_event_type_id
left join hist_users as hist_users_a on hist_users_a.id = he.hist_actor_user_id
left join hist_users as hist_users_t on hist_users_t.id = he.hist_target_user_id
left join hist_workbooks hwb on hwb.id = he.hist_workbook_id
left join hist_views hv on hv.id = he.hist_view_id
left join hist_sites s on s.id = he.hist_actor_site_id
left join (
        select max(workbook_id) as cur_id, name from hist_workbooks
        group by name) cur_wb on cur_wb.name = hwb.name
left join workbooks wb on wb.id = cur_wb.cur_id
left join users u on u.id =  wb.owner_id 
left join system_users su on su.id = u.system_user_id
left join hist_groups hg on hg.id = he.hist_group_id