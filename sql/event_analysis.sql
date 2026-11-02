SELECT
    event_name,
    COUNT(*) AS event_count
FROM
    `firebase-public-project.analytics_153293282.events_20180612`
GROUP BY
    event_name
ORDER BY
    event_count DESC;
