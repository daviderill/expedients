CREATE OR REPLACE FUNCTION "report"."fill_report"(p_id int4)
  RETURNS "pg_catalog"."bool" AS $BODY$

DECLARE
  
	r_exp record;
  v_sql varchar;
	v_sql_1 varchar;
	v_sql_2 varchar;	
	v_aux numeric(15,2);
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
	v_clav_uni numeric(15,2);
	v_clav_plu_2 numeric(15,2);
	v_clav_plu_6 numeric(15,2);
	v_clav_plu_10 numeric(15,2);	
	v_clav_mes numeric(15,2);
	taxa_clav numeric(15,2);
	tot_liq numeric(15,2);
	v_gar_res numeric(15,2);
	v_gar_ser numeric(15,2);
	total numeric(15,2);
	press numeric(15,2);
	bonif_icio numeric(15,2);
	bonif_llic numeric(15,2);

BEGIN

	-- Set system parameter search_path
	SET search_path TO carto, data, report, public;

	-- Borrem contingut previ de les taules de report
	-- Delete previous content of report tables
	DELETE FROM rpt_expedient;

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
	v_clav_uni:= 0;
	v_clav_plu_2:= 0;
	v_clav_plu_6:= 0;
	v_clav_plu_10:= 0;	
	v_clav_mes:= 0;
	v_gar_res:= 0;
	v_gar_ser:= 0;

	-- Get fields of selected 'expedient'
	SELECT exp_om.*, press_om.*
	INTO r_exp
	FROM exp_om INNER JOIN press_om ON exp_om.id = press_om.om_id 
	WHERE exp_om.id = p_id;
		
	-- 'Pressupost' o 'Liquidació Aj.'
	press:= r_exp.pressupost;
	IF r_exp.liq_aj > 0 THEN
		press:= r_exp.liq_aj;
	END IF;

	-- 'ICIO'
	taxa_icio:= press * 0.04;
	IF r_exp.bon_icio THEN
		IF r_exp.bon_icio_value is null THEN
			r_exp.bon_icio_value = 95;
		END IF;
		bonif_icio:= 100 - r_exp.bon_icio_value;
    taxa_icio = (taxa_icio * bonif_icio) / 100;
	END IF;

	-- 'Placa'
	IF r_exp.placa THEN
		taxa_placa:= 12.9;
	END IF;

	-- 'Llicències urbanístiques'
	IF r_exp.plu THEN
		v_plu:= greatest(38.15, press * 0.0096);
	END IF;
	IF r_exp.res THEN
		v_res:= greatest(38.15, press * 0.0094);
	END IF;
	IF r_exp.ende THEN
		v_ende:= press * 0.0367;
	END IF;
	IF r_exp.car IS NOT NULL THEN
		v_car:= r_exp.car * 8.9;
	END IF;
	IF r_exp.mov IS NOT NULL THEN
		v_mov:= r_exp.mov * 0.26;
	END IF;
	IF r_exp.fig IS NOT NULL THEN
		v_fig:= greatest(725.4, r_exp.fig * 0.02);
	END IF;
	IF r_exp.leg THEN
		v_leg:= v_plu + v_car + v_res;
	END IF;
	IF r_exp.par IS NOT NULL THEN
		v_par:= greatest(244, r_exp.fig * 0.02);
	END IF;
	IF r_exp.pro THEN
		v_pro:= 22.2;
	END IF;

	-- 'Clavegueram'
	IF r_exp.clav_uni IS NOT NULL THEN
		v_clav_uni:= r_exp.clav_uni * 390.66;
	END IF;
	IF r_exp.clav_plu IS NOT NULL THEN
		IF r_exp.clav_plu = 2 THEN
			v_clav_plu_2:= 650.76;
		ELSIF r_exp.clav_plu = 6 THEN
			v_clav_plu_6:= 910.86;
		ELSIF r_exp.clav_plu = 10 THEN
			v_clav_plu_10:= 1170.96;
		END IF;
	END IF;
	IF r_exp.clav_mes IS NOT NULL THEN
		v_aux = r_exp.clav_mes - 13;        
		IF v_aux > 0 THEN
				v_clav_mes = 1170.96 + (v_aux * 65.025);
		END IF;
	END IF;
	
	-- 'Taxa llicències urbanístiques'
	--RAISE NOTICE 'valors = % % % % % % % % %', v_plu, v_res, v_ende, v_car, v_mov, v_fig, v_leg, v_par, v_pro;
	taxa_llic:= v_plu + v_res + v_ende + v_car + v_mov + v_fig + v_leg + v_par + v_pro;
	IF r_exp.bon_llic THEN
		IF r_exp.bon_llic_value is null THEN
			r_exp.bon_llic_value = 95;
		END IF;
		bonif_llic:= 100 - r_exp.bon_llic_value;
    taxa_llic = (taxa_llic * bonif_llic) / 100;
	END IF;

	-- 'Taxa clavegueram'
	taxa_clav:= v_clav_uni + v_clav_plu_2 + v_clav_plu_6 + v_clav_plu_10 + v_clav_mes;

	-- 'Total a liquidar'
	tot_liq:= taxa_icio + taxa_placa + taxa_llic + taxa_clav;

	-- 'Garanties'
	IF r_exp.gar_res THEN
		v_gar_res:= greatest(1000, press * 0.01);
	END IF;
	IF r_exp.gar_ser THEN
		v_gar_ser:= greatest(600, press * 0.01);
	END IF;

	-- 'Total'
	total:= tot_liq + v_gar_res + v_gar_ser;

	v_sql_1:= 'INSERT INTO rpt_expedient (om_id, num_exp, parcela, immoble, 
		pressupost, liq_aj, taxa_icio, taxa_placa, 
		v_plu, v_res, v_ende, v_car, v_mov, v_fig, v_leg, v_par, v_pro, taxa_llic,
		clav_uni, v_clav_uni, clav_plu, v_clav_plu_2, v_clav_plu_6, v_clav_plu_10, 
		clav_mes, v_clav_mes, taxa_clav, tot_liq, gar_res, gar_ser, total,
		notif_persona, notif_adreca, notif_cp, notif_poblacio
		) VALUES (';
	v_sql_2:= r_exp.id||', '||quote_nullable(r_exp.num_exp)||', '||quote_nullable(r_exp.parcela_id)||', '||quote_nullable(r_exp.immoble_id)||', 
		'||quote_nullable(r_exp.pressupost)||', '||quote_nullable(r_exp.liq_aj)||', '||taxa_icio||', '||taxa_placa||', 
		'||v_plu||', '||v_res||', '||v_ende||', '||v_car||', '||v_mov||', '||v_fig||', '||v_leg||', '||v_par||', '||v_pro||', '||taxa_llic||',
		'||quote_nullable(r_exp.clav_uni)||', '||v_clav_uni||', '||quote_nullable(r_exp.clav_plu)||', '||v_clav_plu_2||', '||v_clav_plu_6||', '||v_clav_plu_10||',
		'||quote_nullable(r_exp.clav_mes)||', '||v_clav_mes||', '||taxa_clav||', '||tot_liq||', '||v_gar_res||', '||v_gar_ser||', '||total||',
		'||quote_nullable(r_exp.notif_persona)||', '||quote_nullable(r_exp.notif_adreca)||', '||quote_nullable(r_exp.notif_cp)||', '||quote_nullable(r_exp.notif_poblacio);
	
	v_sql:= v_sql_1 || v_sql_2 || ');';
	--RAISE NOTICE 'sql = %', quote_literal(v_sql);
	EXECUTE v_sql;

  RETURN TRUE;

END;

$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100;

ALTER FUNCTION "report"."fill_report"(p_id int4) OWNER TO "gisadmin";