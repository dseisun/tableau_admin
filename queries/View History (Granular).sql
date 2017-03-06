
select 
        hist_users_a.name as action_username, 
        hist_users_t.name as target_username,
        he.created_at,
        het.name as action, 
        hwb.name as workbook,
        hv.name as view,
        now() at time zone 'utc' - he.created_at as time_since_action
        from historical_events he

left join historical_event_types het on het.type_id = he.historical_event_type_id
left join hist_users as hist_users_a on hist_users_a.id = he.hist_actor_user_id
left join hist_users as hist_users_t on hist_users_t.id = he.hist_target_user_id
left join hist_workbooks hwb on hwb.id = he.hist_workbook_id
left join hist_views hv on hv.id = he.hist_view_id
left join hist_sites s on s.id = he.hist_actor_site_id
order by he.created_at desc
