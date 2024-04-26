-- This is a SQL script that ranks country origins of bands in `metal_bands` table,
-- ordered by the number of (non-unique) fans
--
-- Column names in the output will be: `origin` and `nb_fans`
-- The script can be executed on any database
SELECT `origin`, SUM(`fans`) as `nb_fans`
FROM `metal_bands`
    GROUP BY origin
    ORDER BY nb_fans DESC;
