    SELECT ou.ENTTY_RIAD_ID AS "OUID", 
              ou.ENTTY_RIAD_CD AS "RIAD_CODE",  
              ou.NM_ENTTY AS "RIAD_NAME",
              OU.CNTRY as "COUNTRY"
              ,INSTTTNL_SCTR as "ESA_SECTOR"
              ,INSTTTNL_SCTR_DTL as "ESA_SECTOR_DETAILED"
              ,COLLATERALGROUP
              ,CSPP_ASSSSMNT
         FROM RIAD.F_ENTTY@PRIADEXA.PRD.TNS ou 
    where TRUNC (SYSDATE) BETWEEN BSNSS_VLD_FRM AND BSNSS_VLD_T
          AND VRSN_VLD_T = '31-DEC-9999'
          and (		upper(ENTTY_RIAD_CD) = upper('{0}')
				OR  upper(NM_ENTTY) like upper('{1}')
				OR  (ENTTY_RIAD_ID) = ({2})
			  )
    order by OU.CNTRY, ou.NM_ENTTY