SELECT
    table_name,
    PARSE_DATE(
        '%Y%m%d',
        REGEXP_EXTRACT(table_name, r'^events_(\d{8})$')
    ) AS event_date
FROM
    `firebase-public-project.analytics_153293282.INFORMATION_SCHEMA.TABLES`
WHERE
    REGEXP_CONTAINS(table_name, r'^events_\d{8}$')
ORDER BY
    event_date;