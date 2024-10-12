-- Select the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred
SELECT title
FROM movies
WHERE id IN
(
    -- Select movie IDs where Bradley Cooper starred
    SELECT movie_id
    FROM stars
    WHERE person_id =
    (
        -- Find Bradley Cooper's ID
        SELECT id
        FROM people
        WHERE name = 'Bradley Cooper'
    )
)
AND id IN
(
    -- Select movie IDs where Jennifer Lawrence starred
    SELECT movie_id
    FROM stars
    WHERE person_id =
    (
        -- Find Jennifer Lawrence's ID
        SELECT id
        FROM people
        WHERE name = 'Jennifer Lawrence'
    )
);
