SELECT
    PARSE_DATE('%Y%m%d', event_date) AS date,
    COUNT(DISTINCT user_pseudo_id) AS dau,
    COUNT(DISTINCT IF(
        event_name = 'level_complete_quickplay',
        user_pseudo_id,
        NULL
    )) AS successful_players,
    COUNT(DISTINCT IF(
        event_name = 'level_fail_quickplay',
        user_pseudo_id,
        NULL
    )) AS failed_players
FROM
    `firebase-public-project.analytics_153293282.events_*`
WHERE
    _TABLE_SUFFIX BETWEEN @start_date AND @end_date
GROUP BY
    date
ORDER BY
    date;