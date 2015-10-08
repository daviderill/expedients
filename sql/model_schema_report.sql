DROP TABLE IF EXISTS "report"."rpt_expedient" 
CREATE TABLE "data"."rpt_expedient" (
"om_id" int4 NOT NULL,
"num_exp" varchar(15),
"parcela" varchar(14),
"immoble" varchar(20),
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
"v_clav_uni" numeric(15,2),
"clav_plu" int4,
"v_clav_plu" numeric(15,2),
"clav_mes" int4,
"v_clav_mes" numeric(15,2),
"taxa_clav" numeric(15,2),
"tot_liq" numeric(15,2),
"gar_res" numeric(15,2),
"gar_ser" numeric(15,2),
"total" numeric(15,2),
CONSTRAINT "rpt_expedient_pkey" PRIMARY KEY ("om_id")
);


DROP TABLE IF EXISTS "report"."rpt_parcela_total" 
CREATE TABLE "report"."rpt_parcela_total" (
"parcela_id" varchar(14),
"total" int4,
PRIMARY KEY ("parcela_id") 
);