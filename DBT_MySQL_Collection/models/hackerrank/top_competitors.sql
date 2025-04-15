SELECT 
    S.hacker_id,
    H.name
FROM 
    hackerrank.Submissions S
JOIN 
    hackerrank.Hackers H ON S.hacker_id = H.hacker_id
JOIN 
    hackerrank.Challenges C ON S.challenge_id = C.challenge_id
JOIN 
    hackerrank.Difficulty D ON C.difficulty_level = D.difficulty_level
WHERE 
    S.score = D.score
GROUP BY 
    S.hacker_id, H.name
HAVING 
    COUNT(DISTINCT S.challenge_id) > 1 
ORDER BY 
    COUNT(DISTINCT S.challenge_id) DESC, S.hacker_id ASC
