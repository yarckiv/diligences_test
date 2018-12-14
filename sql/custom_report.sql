WITH
    task AS (
    SELECT count(pt.id) AS c_tas, pt.project_id
    FROM project_task AS pt
      LEFT JOIN project_task_type AS ptt ON pt.stage_id = ptt.id
    WHERE ptt.name = 'Testing'
    GROUP BY pt.project_id
  ),
  issue AS (
    SELECT count(pi.id) AS c_is, pi.project_id
    FROM project_issue AS pi
    LEFT JOIN project_task_type AS ptt ON pi.stage_id=ptt.id
    WHERE ptt.name='Backlog'
    GROUP BY pi.project_id
  )
SELECT
  pr.id,
  pr.id        AS project_id,
  pr.state AS state,
  COALESCE((task.c_tas/issue.c_is)/0) AS target
FROM
  project_project AS pr
  LEFT JOIN project_issue AS pi ON pi.project_id=pr.id
  LEFT JOIN issue ON issue.project_id = pr.id
  LEFT JOIN task  ON task.project_id = pr.id