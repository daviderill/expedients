CREATE OR REPLACE FUNCTION "create_rpt_exp_parcela"() RETURNS "pg_catalog"."bool" language plpgsql AS $$

DECLARE
  registro record;
	v_sql varchar;
	v_sql_1 varchar;
	v_sql_2 varchar;	
	taxa_icio numeric(15,2);
	taxa_placa numeric(15,2);
	v_plu numeric(15,2);
	v_res numeric(15,2);
	v_ende numeric(15,2);
	v_car numeric(15,2);
	v_mov numeric(15,2);
	v_fig numeric(15,2);
	v_leg numeric(15,2);
	v_par numeric(15,2);
	v_pro numeric(15,2);
	taxa_llic numeric(15,2);
	
BEGIN

	-- Delete previous content
	v_sql:= 'DELETE FROM rpt_exp_parcela';
	EXECUTE v_sql;

	-- Initialize variables
	taxa_placa:= 0;	
	v_plu:= 0;
	v_res:= 0;
	v_ende:= 0;
	v_car:= 0;
	v_mov:= 0;
	v_fig:= 0;
	v_leg:= 0;
	v_par:= 0;
	v_pro:= 0;

	-- Iterate over 'expedients'
	FOR registro IN 
		SELECT id, num_exp, parcela_id, immoble_id, pressupost, placa, plu, res, ende, car, mov, fig, leg
		FROM exp_om INNER JOIN press_om ON exp_om.id = press_om.om_id 
		ORDER BY id 
	LOOP
		
		--RAISE NOTICE 'aa = %', quote_nullable(registro.immoble_id);
		-- Calculate each variable
		taxa_icio:= registro.pressupost * 0.04;
		IF registro.placa THEN
			taxa_placa:= 12.9;
		END IF;
		IF registro.plu THEN
			v_plu:= greatest(38.15, registro.pressupost * 0.0096);
		END IF;
		IF registro.res THEN
			v_res:= greatest(38.15, registro.pressupost * 0.0094);
		END IF;
		IF registro.ende THEN
			v_ende:= registro.pressupost * 0.0367;
		END IF;
		IF registro.car IS NOT NULL THEN
			v_car:= registro.car * 8.9;
		END IF;
		IF registro.mov IS NOT NULL THEN
			v_mov:= registro.car * 0.26;
		END IF;
		IF registro.fig IS NOT NULL THEN
			v_car:= greatest(725.04, registro.fig * 0.02);
		END IF;
		IF registro.leg THEN
			v_leg:= v_plu + v_car + v_ende;
		END IF;
		IF registro.par IS NOT NULL THEN
			v_par:= greatest(244, registro.fig * 0.02);
		END IF;
		IF registro.pro THEN
			v_pro:= 22.2;
		END IF;
		
		-- Taxa llicència
		taxa_llic:= v_plu + v_res + v_ende + v_car + v_mov + v_fig + v_leg + v_par + v_pro;

		v_sql_1:= 'INSERT INTO rpt_exp_parcela (om_id, num_exp, parcela, immoble, pressupost,
			taxa_icio, taxa_placa, taxa_llic) ';
		v_sql_2:= 'VALUES ('||registro.id||', '||quote_literal(registro.num_exp)||', '||quote_literal(registro.parcela_id)||', '||quote_nullable(registro.immoble_id)||', '||registro.pressupost||', '||taxa_icio||', '||taxa_placa||', '||taxa_llic;
		v_sql:= v_sql_1 || v_sql_2 || ')';

		RAISE NOTICE 'sql = %', quote_literal(v_sql);
		EXECUTE v_sql;
		
	END LOOP;

  RETURN TRUE;

END;
$$;