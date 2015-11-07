DROP VIEW IF EXISTS "data"."v_exp_per_parcela";
CREATE VIEW "data"."v_exp_per_parcela" AS 
 SELECT ur_parcela.id,
    ur_parcela.geom,
    ur_parcela.ninterno,
    ur_parcela.parcela,
    ur_parcela.refcat,
        CASE
            WHEN (( SELECT count(*) AS count
               FROM data.exp_om
              WHERE ((exp_om.parcela_id)::text = (ur_parcela.refcat)::text)) > 0) THEN ( SELECT count(*) AS count
               FROM data.exp_om
              WHERE ((exp_om.parcela_id)::text = (ur_parcela.refcat)::text))
            ELSE NULL::bigint
        END AS total
   FROM carto.ur_parcela;