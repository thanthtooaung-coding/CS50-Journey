-- Select names of all people who starred in a movie with Kevin Bacon (born in 1958), excluding Kevin Bacon
SELECT name
FROM people
WHERE id IN
(
    -- Select person IDs of people who starred in the same movies as Kevin Bacon
    SELECT person_id
    FROM stars
    WHERE movie_id IN
    (
        -- Select movie IDs where Kevin Bacon starred
        SELECT movie_id
        FROM stars
        WHERE person_id =
        (
            -- Find Kevin Bacon's ID (born in 1958)
            SELECT id
            FROM people
            WHERE name = 'Kevin Bacon'
            AND birth = 1958
        )
    )
)
AND name != 'Kevin Bacon';
