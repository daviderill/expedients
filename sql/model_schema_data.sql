DROP TABLE IF EXISTS "data"."estat" 
CREATE TABLE "data"."estat" (
"id" varchar(200),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."exp_om" 
CREATE TABLE "data"."exp_om" (
"id" serial4,
"num_exp" varchar(15),
"data_ent" date,
"data_llic" date,
"tipus_id" varchar(200),
"annex_id" varchar(200),
"tipus_solic_id" varchar(10),
"solic_persona_id" varchar(9),
"solic_juridica_id" varchar(9),
"repre_id" varchar(9),
"redactor_id" varchar(9),
"director_id" varchar(9),
"executor_id" varchar(9),
"constructor" varchar(200),
"visat_num" varchar(50),
"visat_data" date,
"parcela_id" varchar(14),
"immoble_id" varchar(20),
"num_hab" int4,
"notif_adreca" varchar(200),
"notif_poblacio" varchar(100),
"notif_cp" varchar(5),
"observacions" text,
"reg_exp" varchar(15),
"data_liq" date,
"documentacio" text,
"estat_id" varchar(20),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."immoble" 
CREATE TABLE "data"."immoble" (
"id" varchar(20),
"refcat" varchar(14),
"adreca" varchar(200),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."juridica" 
CREATE TABLE "data"."juridica" (
"id" varchar(9),
"rao_social" varchar(200),
"nom" varchar(100),
"cognom_1" varchar(100),
"cognom_2" varchar(100),
"tfon" varchar(15),
"mail" varchar(200),
"adreca" varchar(200),
"poblacio" varchar(100),
"cp" varchar(5),
"observacions" text,
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."persona" 
CREATE TABLE "data"."persona" (
"id" varchar(9),
"nom" varchar(100),
"cognom_1" varchar(100),
"cognom_2" varchar(100),
"tfon" varchar(15),
"mail" varchar(200),
"adreca" varchar(255),
"poblacio" varchar(100),
"cp" varchar(5),
"observacions" text,
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."press_om" 
CREATE TABLE "data"."press_om" (
"om_id" int4,
"pressupost" numeric(15,2),
"placa" bool,
"plu" bool,
"res" bool,
"ende" bool,
"car" numeric(15,2),
"mov" numeric(15,2),
"fig" numeric(15,2),
"leg" bool,
"par" numeric(15,2),
"pro" bool,
"clav_uni" int4,
"clav_plu" int4,
"clav_mes" int4,
"gar_res" bool,
"gar_ser" bool,
"liq_aj" numeric(15,2),
PRIMARY KEY ("om_id") 
);
COMMENT ON COLUMN "data"."press_om"."placa" IS 'OF.7 Taxa Placa';


DROP TABLE IF EXISTS "data"."tecnic" 
CREATE TABLE "data"."tecnic" (
"id" varchar(25),
"dni" varchar(9),
"nom" varchar(100),
"cognom_1" varchar(100),
"cognom_2" varchar(100),
"titulacio" varchar(100),
"observacions" text,
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."tipus_om" 
CREATE TABLE "data"."tipus_om" (
"id" varchar(200),
"obs" varchar(200),
PRIMARY KEY ("id") 
);



ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_tipus_om" FOREIGN KEY ("tipus_id") REFERENCES "data"."tipus_om" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_estat" FOREIGN KEY ("estat_id") REFERENCES "data"."estat" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_persona_1" FOREIGN KEY ("solic_persona_id") REFERENCES "data"."persona" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_juridica_1" FOREIGN KEY ("solic_juridica_id") REFERENCES "data"."juridica" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_persona_2" FOREIGN KEY ("repre_id") REFERENCES "data"."persona" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_tecnic" FOREIGN KEY ("redactor_id") REFERENCES "data"."tecnic" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_tecnic_1" FOREIGN KEY ("director_id") REFERENCES "data"."tecnic" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_tecnic_2" FOREIGN KEY ("executor_id") REFERENCES "data"."tecnic" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_immoble" FOREIGN KEY ("immoble_id") REFERENCES "data"."immoble" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."press_om" ADD CONSTRAINT "fk_press_om_exp_om" FOREIGN KEY ("om_id") REFERENCES "data"."exp_om" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

--ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_ur_parcela" FOREIGN KEY ("parcela_id") REFERENCES "carto"."ur_parcela" ("refcat");


