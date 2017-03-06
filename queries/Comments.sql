select v.*, wb.name, c.comment from comments c
left join views v on v.id = c.commentable_id
left join workbooks wb on wb.id = v.workbook_id
where c.updated_at > current_date - 1
