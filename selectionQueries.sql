/* Used to get average sentiment by keyword and day */
SELECT
DATE_PART('doy', post_date) as day_of_year,
keyword,
AVG(sentiment) as avg_sentiment

FROM
bluesky_post_data

WHERE
keyword = ''

GROUP BY
keyword,
DATE_PART('doy',post_date)

ORDER BY
DATE_PART('doy', post_date) ASC
