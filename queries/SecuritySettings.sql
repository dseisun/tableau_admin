select 
        s.name as site_name,
        p.name as project_name,
        wb.name as workbook_name, 
        su.name as user_name,
        c.name as capability_name,
        'Group' as permissioned_via
from next_gen_permissions ngpg
inner join workbooks wb on wb.id = ngpg.authorizable_id and ngpg.authorizable_type = 'Workbook'
inner join group_users gu on gu.group_id = ngpg.grantee_id and ngpg.grantee_type = 'Group'
inner join users u on u.id = gu.user_id
inner join system_users su on su.id = u.system_user_id
inner join projects p on p.id = wb.project_id
inner join sites s on s.id = wb.site_id
inner join capabilities c on c.id = ngpg.capability_id
where ngpg.permission = 1

union all
select 
        s.name as site_name,
        p.name as project_name,
        wb.name as workbook_name, 
        su.name as user_name,
        c.name as capability_name,
        'User' as permissioned_via
from next_gen_permissions ngpu
inner join workbooks wb on wb.id = ngpu.authorizable_id and ngpu.authorizable_type = 'Workbook'
inner join users u on u.id = ngpu.grantee_id and ngpu.grantee_type = 'User'
inner join system_users su on su.id = u.system_user_id
inner join projects p on p.id = wb.project_id
inner join sites s on s.id = wb.site_id
inner join capabilities c on c.id = ngpu.capability_id
where ngpu.permission = 3
