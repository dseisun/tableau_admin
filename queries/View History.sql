select 
        su.name as "Username", 
        u.created_at as "UserCreateDate", 
        v.name as "Viewname", 
        v.repository_url as "ViewUrl",
        v.created_at as "ViewCreateDate",
        v.sheettype as "ViewType",
        vs.nviews as "ViewCount",
        vs.time as "ViewTime",
        lr.name as "UserLicenseLevel",
        w.name as "Workbook Name",
        w.site_id,
        su_owner.name as "Workbook Owner"
        
        
from users u
inner join views_stats vs on vs.user_id = u.id
left join system_users su on su.id = u.system_user_id
left join views v on v.id = vs.view_id
left join workbooks w on w.id = v.workbook_id
left join users u_owner on u_owner.id = w.owner_id
left join system_users su_owner on u_owner.system_user_id = su_owner.id
left join licensing_roles lr on lr.id = u.licensing_role_id
