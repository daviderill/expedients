ALTER TABLE "data"."exp_om"
ADD COLUMN "reg_ent" varchar(25),
ADD COLUMN "data_liq" date;

ALTER TABLE "data"."exp_om"
ADD COLUMN "documentacio" text;

ALTER TABLE "data"."press_om"
ADD COLUMN "liq_aj" numeric(15,2);

ALTER TABLE "data"."exp_om"
ADD COLUMN "estat_id" varchar(200);
ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_estat" FOREIGN KEY ("estat_id") REFERENCES "data"."estat" ("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "data"."exp_om"
DROP COLUMN "annex_id";

-- 15/10/2015
ALTER TABLE "data"."tecnic"
DROP COLUMN "observacions",
ADD COLUMN "num_colegiat" varchar(100),
ADD COLUMN "observacions" text;


-- 16/10/2015
ALTER TABLE "data"."exp_om"
DROP CONSTRAINT "fk_exp_om_immoble";

DROP TABLE IF EXISTS "data"."immoble" ; 

DELETE FROM data.ibi USING data.ibi AS aux
WHERE data.ibi.refcat20 = aux.refcat20 AND data.ibi.id < aux.id;
DELETE FROM data.ibi WHERE refcat20 is null;
ALTER TABLE "data"."ibi"
DROP CONSTRAINT "ibi_pkey";
ALTER TABLE "data"."ibi"
ADD PRIMARY KEY ("refcat20");

UPDATE "data"."exp_om" SET immoble_id = null WHERE immoble_id = '';

ALTER TABLE "data"."exp_om" ADD CONSTRAINT "fk_exp_om_immoble" FOREIGN KEY ("immoble_id") REFERENCES "data"."ibi" ("refcat20") ON DELETE SET NULL ON UPDATE CASCADE;

UPDATE "data".ibi SET carrer_t = trim(carrer_t), adreca_t = trim(adreca_t);

ALTER TABLE "data"."press_om"
ADD COLUMN "bon_icio" bool,
ADD COLUMN "bon_llic" bool,
ADD COLUMN "total_press" numeric(15,2),
ADD COLUMN "total_liq" numeric(15,2);


-- 20/10/2015
ALTER TABLE "data"."exp_om"
ADD COLUMN "notif_persona" varchar(200);


-- 22/10/2015
ALTER TABLE "data"."ibi"
DROP COLUMN "id";

CREATE OR REPLACE FUNCTION "data"."create_immoble_extra"()
  RETURNS "pg_catalog"."bool" AS $BODY$

DECLARE
    registro  record;
	v_sql varchar;
	refcat20 varchar;
	
BEGIN

	FOR registro IN 
		SELECT DISTINCT(refcat14) FROM "data".ibi ORDER BY refcat14
	LOOP
		refcat20:= registro.refcat14||'-9999/99';
		v_sql:= 'INSERT INTO data.ibi (refcat14, refcat20) VALUES ('||quote_literal(registro.refcat14)||', '||quote_literal(refcat20)||')';
		EXECUTE v_sql;
	END LOOP;

    RETURN TRUE;

END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE COST 100;




