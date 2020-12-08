with

    single_snapshot_uc AS -- returns latest snapshot_date of UC
        (SELECT MAX(snapshot_date)                           AS snapshot_date,
                to_number(EXTRACT(MONTH FROM MAX(snapshot_date))) AS "MONTH",
                to_number(to_char(MAX(snapshot_date), 'Q'))       AS quarter,
                EXTRACT(YEAR FROM MAX(snapshot_date))             AS "YEAR"
           FROM collateral.mv_snapshot_date
          WHERE snapshot_date BETWEEN trunc(SYSDATE-20) AND trunc(SYSDATE-6) /*     <<<<<<< returns the latest UC snapshot date (excluding today) <<<<<<< */
            AND to_char(snapshot_date, 'DY') = 'THU'
        )
, 
/* change required module here and use TIME_HORIZON in all queries afterwards */
time_horizon AS
(
  SELECT * FROM single_snapshot_uc  /* <<<<<<< change desired time frame module here */
)
    ,
    uc AS
        (SELECT snapshot_date, mfi_id, max(MFI_NAME) as MFI_NAME, sum(coll_value_after_haircuts) as cvah
           FROM collateral.mv_granular_collateral
          INNER JOIN time_horizon USING (snapshot_date) 
          WHERE 1=1
            /* custom filter: */
            AND (1=1) -- add additional filters here in brackets
            and mfi_id in ({0})
          group by snapshot_date, mfi_id, mfi_name
        )
,
mpo as
(select snapshot_date, mfi_id, sum(credit_outstanding) as mpo
from collateral.credit_outstanding
INNER JOIN time_horizon USING (snapshot_date) 
where mfi_id in ({0})
group by snapshot_date, mfi_id
)
,
ea as
(select snapshot_date, issuer_code as mfi_id, max(issuer_name) as issuer_name, sum(nominal_value_outstanding_) as nvo
from collateral.all_assets
INNER JOIN time_horizon USING (snapshot_date) 
where status='E'
and issuer_code in ({0})
group by snapshot_date, issuer_code
)

        
  SELECT SNAPSHOT_DATE, MFI_ID, coalesce(issuer_name,MFI_NAME) as MFI_NAME, nvl(NVO,0) as nvo, nvl(MPO,0) as mpo, nvl(CVAH,0) as cvah
    FROM ea
    full outer join mpo using (snapshot_date,mfi_id)
    full outer join uc using (snapshot_date,mfi_id)
	where 
		NVO>0
		or MPO>0
		or CVAH>0
		