DROP TABLE IF EXISTS "data"."estat" CASCADE;
CREATE TABLE "data"."estat" (
"id" varchar(200),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."exp_om" CASCADE;
CREATE TABLE "data"."exp_om" (
"id" serial4,
"num_exp" varchar(15),
"data_ent" date,
"data_llic" date,
"tipus_id" varchar(200),
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
"immoble_id" varchar(30),
"num_hab" int4,
"notif_adreca" varchar(200),
"notif_poblacio" varchar(100),
"notif_cp" varchar(5),
"observacions" text,
"reg_ent" varchar(25),
"data_liq" date,
"documentacio" text,
"estat_id" varchar(200),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."ibi";
CREATE TABLE "data"."ibi" (
"id" int4 NOT NULL,
"refcat14" varchar,
"refcat20" varchar,
"cod_via" int4,
"sigles_t" varchar,
"carrer_t" varchar,
"numero_t" int4,
"duplicat_t" varchar,
"escala_t" varchar,
"pis_t" varchar,
"porta_t" varchar,
"adreca_t" varchar,
CONSTRAINT "ibi_pkey" PRIMARY KEY ("refcat20")
);


DROP TABLE IF EXISTS "data"."immoble";
CREATE TABLE "data"."immoble" (
"id" varchar(20),
"refcat" varchar(14),
"adreca" varchar(200),
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."juridica";
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


DROP TABLE IF EXISTS "data"."llistat_carrerer_ibi"; 
CREATE TABLE "data"."llistat_carrerer_ibi" (
"id_0" SERIAL,
"id" int4,
"ORDRE" int4,
"SECTOR O URBANITZACIO" varchar,
"ILLA CADASTRAL" int4,
"rc" varchar,
"full *" varchar,
"full" varchar,
"refcat14" varchar,
"n" int4,
"i" varchar,
"Referència cadastral" varchar,
"Classe del bé immoble" varchar,
"CODI VIA" int4,
"Sigles T" varchar,
"Carrer T" varchar,
"Numero T" int4,
"Duplicat T" varchar,
"Escala T" varchar,
"Pis T" varchar,
"Porta T" varchar,
"Adreça tributària" varchar,
"Dni" varchar,
"Nom" varchar,
"Sigles F" varchar,
"Carrer F" varchar,
"Numero F" int4,
"Duplicat F" varchar,
"Escala F" varchar,
"Pis F" varchar,
"Porta F" varchar,
"Adreça fiscal" varchar,
"CP fiscal" int4,
"Codi municipi fiscal" int4,
"Nom municipi fiscal" varchar,
"Superfície del sòl" int4,
"Superfície de la construcció" int4,
"Superfície construcció càrrec" int4,
"Tipologia constructiva" varchar,
"Any de construcció" varchar,
"Valor cadastral Total" float8,
"Valor del sòl" float8,
"Valor de la construcció" float8,
"Base liquidable" float8,
"Tipus gravamen" float8,
"Q. Íntegra" float8,
"Valor Base" float8,
"Ús" varchar,
"Divisió Quotes" varchar,
"Coeficient Divisió" varchar,
"QI Divisió" float8,
"Quota Líquida Inicial" float8,
"Quota Líquida Max" int4,
"Import Bonificació" float8,
"Quota Líquida Rebut" float8,
"NIF Cotitular" varchar,
"B74.2 - Càrrec Anterior" int4,
"B74.2 - Núm. Valor Anterior" varchar,
"B74.2 - Import Bonificat" int4,
"1-Codi Bonificació" varchar,
"1-Descripció Bonificació" varchar,
"1-Any Inici Bonificació" int4,
"1-Any Fi Bonificació" int4,
"1-Import Bonificació" float8,
"2-Codi Bonificació" varchar,
"2-Descripció Bonificació" varchar,
"2-Any Inici Bonificació" int4,
"2-Any Fi Bonificació" int4,
"2-Import Bonificació" int4,
"3-Codi Bonificació" varchar,
"3-Descripció Bonificació" varchar,
"3-Any Inici Bonificació" int4,
"3-Any Fi Bonificació" int4,
"3-Import Bonificació" int4,
"VC Bonificat" int4,
"Clau Bonif VC" varchar,
"Import Bonif VC" int4,
CONSTRAINT "llistat_carrerer_ibi_pkey" PRIMARY KEY ("id_0")
);


DROP TABLE IF EXISTS "data"."persona"; 
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


DROP TABLE IF EXISTS "data"."press_om"; 
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


DROP TABLE IF EXISTS "data"."tecnic"; 
CREATE TABLE "data"."tecnic" (
"id" varchar(25),
"dni" varchar(9),
"nom" varchar(100),
"cognom_1" varchar(100),
"cognom_2" varchar(100),
"titulacio" varchar(100),
"num_colegiat" varchar(100),
"observacions" text,
PRIMARY KEY ("id") 
);


DROP TABLE IF EXISTS "data"."tipus_om"; 
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

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_immoble" FOREIGN KEY ("immoble_id") REFERENCES "data"."ibi" ("refcat20") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."press_om" ADD CONSTRAINT "fk_press_om_exp_om" FOREIGN KEY ("om_id") REFERENCES "data"."exp_om" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

--ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_ur_parcela" FOREIGN KEY ("parcela_id") REFERENCES "carto"."ur_parcela" ("refcat");


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
   FROM ur_parcela;