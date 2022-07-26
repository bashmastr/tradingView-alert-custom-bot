-- volumetric return if diff under 60 SECOND

SELECT *,
TIMESTAMPDIFF(SECOND, v1.TIME, v2.TIME) as diff
	FROM volumetric v1 ,  volumetric v2

where v1.TICKER = 'FLMUSDT'
and v1.TICKER =  v2.TICKER
and v1.ID <> v2.ID
and v2.ID = (SELECT MAX(ID) FROM volumetric where TICKER = 'FLMUSDT')
and TIMESTAMPDIFF(SECOND, v1.TIME, v2.TIME) <= 61;