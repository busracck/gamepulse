SELECT
    user_pseudo_id,
    COUNT(DISTINCT event_name) AS result_types
FROM `firebase-public-project.analytics_153293282.events_20180612`
WHERE event_name IN (
    'level_complete_quickplay',
    'level_fail_quickplay'
)
GROUP BY user_pseudo_id
HAVING COUNT(DISTINCT event_name) = 2;