-- Write query to get number of assignments for each state
SELECT state, COUNT(*) AS state_count
FROM assignments
GROUP BY state;
