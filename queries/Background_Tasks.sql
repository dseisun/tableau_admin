select 
        title,
        subtitle,
        finish_code,
        bj.priority,
        progress,
        timezone('utc', started_at) as started_at_PST,
        timezone('utc', completed_at) as completed_at_PST,
        now() at time zone 'utc' - completed_at as time_since_completion,
        completed_at - started_at as refresh_time,
        notes,
        su.name as wb_owner
from background_jobs bj
left join workbooks wb on wb.name = bj.title and bj.site_id = wb.site_id
left join users u on u.id =  wb.owner_id 
left join sites si on si.id = wb.site_id
left join system_users su on su.id = u.system_user_id
where job_name in ('Refresh Extracts', 'Increment Extracts')
order by started_at_pst desc