CREATE OR REPLACE FUNCTION "report"."create_report_3"()
  RETURNS "pg_catalog"."void" AS $BODY$

BEGIN

	DROP TABLE IF EXISTS "report"."rpt_report_3";
	CREATE TABLE "report"."rpt_report_3" (
	"om_id" int4 NOT NULL,
	"num_exp" varchar,
	"sol_nif" varchar, 
	"sol_name" varchar, 
	"adreca_t" varchar, 
	"cp" varchar,
	"poblacio" varchar,
	"data_ent" varchar,
	"reg_ent" varchar,
	"parcela" varchar,
	"immoble" varchar,
	"executor_name" varchar,
	"visat_num" varchar,
	"observacions" varchar,
	"total_press" numeric(15,2),
	"liq_prov" numeric(15,2),
	"taxa_placa" numeric(15,2),
	"taxa_icio" numeric(15,2), 
	"taxa_llic" numeric(15,2),
	"gar_ser" numeric(15,2),
	"gar_res" numeric(15,2),
	CONSTRAINT "rpt_report_3_pkey" PRIMARY KEY ("om_id")
	);

END;
 
$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100
;

ALTER FUNCTION "report"."create_report_3"() OWNER TO "gisadmin";