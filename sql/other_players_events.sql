SELECT
    event_name,
    COUNT(*) AS event_count
FROM `firebase-public-project.analytics_153293282.events_20180612`
WHERE user_pseudo_id IN (
    SELECT DISTINCT user_pseudo_id
    FROM `firebase-public-project.analytics_153293282.events_20180612`
    WHERE user_pseudo_id NOT IN (
        SELECT user_pseudo_id
        FROM `firebase-public-project.analytics_153293282.events_20180612`
        WHERE event_name IN (
            'level_complete_quickplay',
            'level_fail_quickplay'
        )
    )
)
GROUP BY event_name
ORDER BY event_count DESC;