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




