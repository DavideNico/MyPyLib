with
left_id as (
	select ouid as ouid1, IDENTIFIER_CODE as riad_code1 from mfi.V_RIAD_ORG_IDENT
)
,
right_id as (
	select ouid as ouid2, IDENTIFIER_CODE as riad_code2 from mfi.V_RIAD_ORG_IDENT
)
,
close_links as (
select distinct ouid1, riad_code1, name as name1, country as country1, ouid2, riad_code2, name_2 as name2, country_2 as country2, CLOSELINK_DATE, OWNERSHIP_PERCENTAGE
from MFI.mv_cl_current
inner join left_id using (ouid1)
inner join right_id using (ouid2)
)

select * from close_links 
where riad_code1 = '{}'
and riad_code2 = '{}'



