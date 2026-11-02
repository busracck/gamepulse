SELECT
    COUNT(DISTINCT user_pseudo_id) AS quickplay_players
FROM `firebase-public-project.analytics_153293282.events_20180612`
WHERE event_name = 'level_start_quickplay'
AND user_pseudo_id NOT IN (
    SELECT user_pseudo_id
    FROM `firebase-public-project.analytics_153293282.events_20180612`
    WHERE event_name IN (
        'level_complete_quickplay',
        'level_fail_quickplay'
    )
);