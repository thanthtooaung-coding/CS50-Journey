-- Select the titles of the five highest-rated movies starring Chadwick Boseman
SELECT title
FROM movies
WHERE id IN
(
    -- Select movie IDs that Chadwick Boseman starred in
    SELECT movie_id
    FROM stars
    WHERE person_id =
    (
        -- Find Chadwick Boseman's ID
        SELECT id
        FROM people
        WHERE name = 'Chadwick Boseman'
    )
)
ORDER BY
(
    -- Get the ratings of the movies
    SELECT rating
    FROM ratings
    WHERE movie_id = movies.id
) DESC
LIMIT 5;
