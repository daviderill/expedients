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
  LANGUAGE 'plpgsql' VOLATILE COST 100
;

ALTER FUNCTION "data"."create_immoble_extra"() OWNER TO "gisadmin";