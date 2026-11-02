SELECT
    user_pseudo_id,
    event_name,
    COUNT(*) AS event_count
FROM `firebase-public-project.analytics_153293282.events_20180612`
WHERE event_name IN (
    'level_complete_quickplay',
    'level_fail_quickplay'
)
GROUP BY user_pseudo_id, event_name
ORDER BY user_pseudo_id;