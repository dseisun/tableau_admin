select 
        
        su.name as user_name, 
        su.friendly_name, 
        su.created_at, 
        lr.name as licenese_level, 
        max(users.login_at) as last_login,
        now() at time zone 'utc' - max(users.login_at) as time_since_login
         from users
inner join licensing_roles lr on lr.id = users.licensing_role_id
inner join system_users su on su.id = users.system_user_id
where lr.id = 2
group by su.name, 
        su.friendly_name,  
        su.created_at, 
        lr.name
order by coalesce(max(users.login_at), '2010-01-01') desc