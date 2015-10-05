ALTER TABLE "data"."exp_om"
ADD COLUMN "reg_ent" varchar(25),
ADD COLUMN "data_liq" date;

ALTER TABLE "data"."exp_om"
ADD COLUMN "documentacio" text;

ALTER TABLE "data"."press_om"
ADD COLUMN "liq_aj" numeric(15,2);

