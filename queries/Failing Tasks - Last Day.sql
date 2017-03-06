select 
        title,
        completed_at at time zone 'utc' as time_since_failure_pst,
        wb.updated_at,
        coalesce(su.name || '@twitter.com', 'dseisun@twitter.com') as wb_owner,
        notes
from background_jobs bj
left join workbooks wb on wb.name = bj.title and bj.site_id = wb.site_id
left join users u on u.id =  wb.owner_id 
left join system_users su on su.id = u.system_user_id
where job_name in ('Refresh Extracts', 'Increment Extracts')
and finish_code = 1
and progress = 100
and now() at time zone 'utc' < completed_at + interval '1 day'
order by completed_at desc