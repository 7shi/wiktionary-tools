SELECT RANK() OVER(ORDER BY cnt DESC) AS rank, name, cnt FROM langname
INNER JOIN (
    SELECT lid, COUNT(lid) as cnt FROM idlang GROUP BY lid ORDER BY cnt DESC
) AS langcnt ON langname.lid = langcnt.lid;
