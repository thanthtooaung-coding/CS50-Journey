-- Keep a log of any SQL queries you execute as you solve the mystery.

-- For understanding all table structures of the database
.schema

-- In the given, All you know is that the theft took place on July 28, 2023 and that it took place on Humphrey Street.
SELECT id, description FROM crime_scene_reports
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND street = "Humphrey Street";

-- (1) Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--    Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- (2) Littering took place at 16:36. No known witnesses.

-- Reading the transcript of interviews
SELECT name, transcript FROM interviews
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND transcript LIKE "%bakery%";

-- Ruth     - Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--            If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene - I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--          I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond - As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
--           I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--           The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Seeing the security logs of the bakery to get more info about the car in which the thief drove away at 10:15 and within ten minutes that Ruth told
SELECT hour, minute, activity, license_plate FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute > 15
    AND minute <= 25;

-- Looking at the ATM transactions that Eugene told
SELECT account_number, transaction_type, amount FROM atm_transactions
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND atm_location = "Leggett Street";

-- Seeing the phone_calls on the crime day that about less than one minute that Raymond told
SELECT caller, receiver FROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration < 60;

-- Checking the earliest flight out of Fiftyville tomorrow that Raymond told
SELECT id as flight_id, hour, minute FROM flights
    WHERE year = 2023
    AND month = 7
    AND day = 29
    AND origin_airport_id IN (
        SELECT id FROM airports
            WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute;
-- +-----------+------+--------+
-- | flight_id | hour | minute |
-- +-----------+------+--------+
-- | 36        | 8    | 20     |
-- +-----------+------+--------+

 -- Finding who purchase the flight ticket at July 28, 2023
SELECT passport_number FROM passengers
    WHERE flight_id = 36;

SELECT city FROM airports
    WHERE id =
        (SELECT destination_airport_id FROM flights
            WHERE id = 36);

-- +---------------+
-- |     city      |
-- +---------------+
-- | New York City |
-- +---------------+
-- The city the thief ESCAPED TO: New York City

-- Finding the name and phone number of the name
SELECT name, phone_number FROM people
    WHERE license_plate IN
        -- Ruth told
        (SELECT license_plate FROM bakery_security_logs
            WHERE year = 2023
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute > 15
            AND minute <= 25)
    AND id IN
        -- Eugene told
        (SELECT person_id FROM bank_accounts
            WHERE account_number IN
                (SELECT account_number FROM atm_transactions
                    WHERE year = 2023
                    AND month = 7
                    AND day = 28
                    AND atm_location = "Leggett Street"
                    AND transaction_type = "withdraw"))
    AND phone_number IN
        -- Raymond told
        (SELECT caller FROM phone_calls
            WHERE year = 2023
            AND month = 7
            AND day = 28
            AND duration < 60)
    AND passport_number IN
        (SELECT passport_number FROM passengers
            WHERE flight_id = 36);
-- +-------+----------------+
-- | name  |  phone_number  |
-- +-------+----------------+
-- | Bruce | (367) 555-5533 |
-- +-------+----------------+
-- The THIEF is: Bruce

SELECT name FROM people
    WHERE phone_number = (
        SELECT receiver
        FROM phone_calls
        WHERE "(367) 555-5533" = caller
        AND year = 2023
        AND month = 7
        AND day = 28
        AND duration < 60
    );
-- +-------+
-- | name  |
-- +-------+
-- | Robin |
-- +-------+
-- The ACCOMPLICE is: Robin
