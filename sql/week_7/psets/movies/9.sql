-- Select names
SELECT name
FROM people
WHERE id IN
    (
        -- Select person IDs
        SELECT person_id
        FROM stars
        WHERE movie_id IN
        (
            -- Select movie IDs released in 2004
            SELECT id
            FROM movies
            WHERE year = 2004
        )
    )
ORDER BY birth;
