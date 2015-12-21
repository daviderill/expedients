CREATE OR REPLACE FUNCTION "report"."create_report"()
  RETURNS "pg_catalog"."void" AS $BODY$

BEGIN

DROP TABLE IF EXISTS "report"."rpt_expedient";
CREATE TABLE "report"."rpt_expedient" (
"om_id" int4 NOT NULL,
"num_exp" varchar,
"parcela" varchar,
"immoble" varchar,
"pressupost" numeric(15,2),
"liq_aj" numeric(15,2),
"taxa_icio" numeric(15,2),
"taxa_placa" numeric(15,2),
"v_plu" numeric(15,2),
"v_res" numeric(15,2),
"v_ende" numeric(15,2),
"v_car" numeric(15,2),
"v_mov" numeric(15,2),
"v_fig" numeric(15,2),
"v_leg" numeric(15,2),
"v_par" numeric(15,2),
"v_pro" numeric(15,2),
"taxa_llic" numeric(15,2),
"clav_uni" int4,
"v_clav_uni" numeric (15,2),
"clav_plu" int4,
"v_clav_plu_2" numeric (15,2),
"v_clav_plu_6" numeric (15,2),
"v_clav_plu_10" numeric (15,2),
"clav_mes" int4,
"v_clav_mes" numeric (15,2),
"taxa_clav" numeric(15,2),
"tot_liq" numeric(15,2),
"gar_res" numeric(15,2),
"gar_ser" numeric(15,2),
"total" numeric(15,2),
"notif_persona" varchar,
"notif_adreca" varchar,
"notif_cp" varchar,
"notif_poblacio" varchar,
CONSTRAINT "rpt_expedient_pkey" PRIMARY KEY ("om_id")
);

END;
 
$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100;

ALTER FUNCTION "report"."create_report"() OWNER TO "gisadmin";