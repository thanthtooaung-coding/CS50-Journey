-- Select names
SELECT name
FROM people
WHERE id IN
(
    -- Select person IDs of directors
    SELECT person_id
    FROM directors
    WHERE movie_id IN
    (
        -- Select movie IDs with a rating of at least 9.0
        SELECT movie_id
        FROM ratings
        WHERE rating >= 9.0
    )
);
