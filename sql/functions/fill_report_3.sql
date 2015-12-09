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
        exp_om."id",
        exp_om.num_exp,
        persona.id, 
        COALESCE(persona.nom, '') || ' ' || COALESCE (persona.cognom_1, '') || ' ' || COALESCE(persona.cognom_2, '') AS sol_name,    
        exp_om.data_ent,
        exp_om.reg_ent,
        exp_om.parcela_id,
        exp_om.immoble_id,     
        COALESCE(tecnic.nom, '') || ' ' || COALESCE (tecnic.cognom_1, '') || ' ' || COALESCE(tecnic.cognom_2, '') AS executor_name,
        exp_om.visat_num,
        press_om.total_press,
        taxa_placa + taxa_icio + taxa_llic AS liq_prov,
        taxa_placa, taxa_icio, taxa_llic, rpt_expedient.gar_ser, rpt_expedient.gar_res
    FROM exp_om
    INNER JOIN press_om ON exp_om."id" = press_om.om_id
    LEFT JOIN persona ON exp_om.solic_persona_id = persona."id"
    LEFT JOIN tecnic ON exp_om.executor_id = tecnic."id"
    LEFT JOIN rpt_expedient ON exp_om."id" = rpt_expedient.om_id
	WHERE exp_om.id = p_id);

    RETURN TRUE;

END;

$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100;
