WITH global_head AS
  (SELECT distinct gh_ouid FROM mfi.MV_CNG_CURRENT WHERE ORG_RIAD_CODE = '{0}' or GH_RIAD_CODE = '{0}'
  )

SELECT *
FROM mfi.MV_CNG_CURRENT otr
WHERE otr.gh_ouid = (SELECT global_head.gh_ouid FROM global_head)
order by case when otr.dp_ouid = otr.gh_ouid then 0 else 1 end asc, otr.dp_RIAD_CODE asc, otr.ORG_RIAD_CODE asc