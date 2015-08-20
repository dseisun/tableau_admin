--Find the person who published the most reports in a given project
SELECT *
FROM (
  SELECT
     s.name site_name
   , p.name project_name
   , su_owner.name owner_name
   , su_owner.name || '@twitter.com' owner_email
   , COUNT(1) num, ROW_NUMBER()
       OVER(PARTITION BY s.name, p.name ORDER BY count(1) DESC) AS project_rank
  FROM workbooks wb
  LEFT JOIN projects p
    ON p.id = wb.project_id
  LEFT JOIN sites s
    ON s.id = p.site_id
  LEFT JOIN users u_owner
    ON u_owner.id = wb.owner_id
  LEFT JOIN system_users su_owner
    ON u_owner.system_user_id = su_owner.id
  GROUP by su_owner.name, p.name, s.name
) x
WHERE project_rank = 1
