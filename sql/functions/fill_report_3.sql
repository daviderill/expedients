CREATE OR REPLACE FUNCTION "report"."fill_report_3"(p_id int4)
  RETURNS "pg_catalog"."bool" AS $BODY$

BEGIN

    -- Set system parameter search_path
    SET search_path TO carto, data, report, public;

    -- Delete previous content of report tables
    DELETE FROM rpt_report_3;
  
    -- Get fields of selected 'expedient'
    INSERT INTO rpt_report_3 (
        SELECT
            exp_om.id, exp_om.num_exp,
            CASE WHEN tipus_solic_id = 'persona' THEN solic_persona_id ELSE repre_id END AS notif_nif, 
            notif_persona, notif_adreca, notif_cp, notif_poblacio,
            data_ent, reg_ent, parcela_id, immoble_id,     
            COALESCE(tecnic.nom, '') || ' ' || COALESCE (tecnic.cognom_1, '') || ' ' || COALESCE(tecnic.cognom_2, '') AS executor_name,
            visat_num, exp_om.observacions,
            press_om.total_press,
            taxa_placa + taxa_icio + taxa_llic AS liq_prov, taxa_placa, taxa_icio, taxa_llic, 
            rpt_expedient.gar_ser, rpt_expedient.gar_res
        FROM exp_om
        INNER JOIN press_om ON exp_om.id = press_om.om_id
        LEFT JOIN tecnic ON exp_om.redactor_id = tecnic.id
        LEFT JOIN rpt_expedient ON exp_om.id = rpt_expedient.om_id
        WHERE exp_om.id = p_id);

    RETURN TRUE;

END;

$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100
;

ALTER FUNCTION "report"."fill_report_3"(p_id int4) OWNER TO "gisadmin";