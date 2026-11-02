SELECT
    COUNT(DISTINCT user_pseudo_id) AS failed_players
FROM `firebase-public-project.analytics_153293282.events_20180612`
WHERE event_name = 'level_fail_quickplay';