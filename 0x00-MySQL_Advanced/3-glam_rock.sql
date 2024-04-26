-- This is a SQL script that lists all bands with "Glam rock" as their main style,
-- ranked by their longevity till year 2022
--
-- Column names in the output will be: `band_name` and `lifespan`
-- Attributes `formed` and `split` are used for computing the lifespan
-- The script can be executed on any database
SELECT `band_name`,
        (IF(`split` IS NULL, 2022, `split`) - `formed`) as `lifespan`
FROM `metal_bands`
WHERE `style` LIKE "%Glam rock%"
ORDER BY `lifespan` DESC;
