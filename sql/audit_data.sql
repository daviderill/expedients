-- An audit history is important on most tables. Provide an audit trigger that logs to
-- a dedicated audit table for the major relations.
-- This code is generic and not depend on application roles or structures. Is based on:
--   http://wiki.postgresql.org/wiki/Audit_trigger_91plus

-- Enable extension hstore
CREATE EXTENSION IF NOT EXISTS hstore;

-- Create schema for auditing
CREATE SCHEMA IF NOT EXISTS audit;
REVOKE ALL ON SCHEMA audit FROM public;
COMMENT ON SCHEMA audit IS 'Out-of-table audit/history logging tables and trigger functions';

--
-- Audited data. Lots of information is available, it's just a matter of how much
-- you really want to record. See:
--   http://www.postgresql.org/docs/9.1/static/functions-info.html
--
-- Remember, every column you add takes up more audit table space and slows audit inserts.
--
-- Every index you add has a big impact too, so avoid adding indexes to the
-- audit table unless you REALLY need them. The hstore GIST indexes are
-- particularly expensive.
--
-- It is sometimes worth copying the audit table, or a coarse subset of it that
-- you're interested in, into a temporary table where you CREATE any useful
-- indexes and do your analysis.
--
CREATE TABLE IF NOT EXISTS audit.logged_actions (
    id bigserial primary key,
    schema_name text not null,
    table_name text not null,
    relid oid not null,
    user_name text,
    addr inet,
    transaction_id bigint,
    action_tstamp_tx TIMESTAMP WITH TIME ZONE NOT NULL,
    action_tstamp_stm TIMESTAMP WITH TIME ZONE NOT NULL,
    action_tstamp_clk TIMESTAMP WITH TIME ZONE NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('I','D','U','T')),
    query text,
    row_data hstore,
    changed_fields hstore,
    statement_only boolean not null
);

REVOKE ALL ON audit.logged_actions FROM public;

COMMENT ON TABLE audit.logged_actions IS 'History of auditable actions on audited tables, from audit.if_modified_func()';
COMMENT ON COLUMN audit.logged_actions.id IS 'Unique identifier for each auditable event';
COMMENT ON COLUMN audit.logged_actions.schema_name IS 'Database schema audited table for this event is in';
COMMENT ON COLUMN audit.logged_actions.table_name IS 'Non-schema-qualified table name of table event occured in';
COMMENT ON COLUMN audit.logged_actions.relid IS 'Table OID. Changes with drop/create. Get with ''tablename''::regclass';
COMMENT ON COLUMN audit.logged_actions.user_name IS 'Login / session user whose statement caused the audited event';
COMMENT ON COLUMN audit.logged_actions.addr IS 'IP address of client that issued query. Null for unix domain socket.';
COMMENT ON COLUMN audit.logged_actions.transaction_id IS 'Identifier of transaction that made the change. May wrap, but unique paired with action_tstamp_tx.';
COMMENT ON COLUMN audit.logged_actions.action_tstamp_tx IS 'Transaction start timestamp for tx in which audited event occurred';
COMMENT ON COLUMN audit.logged_actions.action_tstamp_stm IS 'Statement start timestamp for tx in which audited event occurred';
COMMENT ON COLUMN audit.logged_actions.action_tstamp_clk IS 'Wall clock time at which audited event''s trigger call occurred';
COMMENT ON COLUMN audit.logged_actions.action IS 'Action type; I = insert, D = delete, U = update, T = truncate';
COMMENT ON COLUMN audit.logged_actions.query IS 'Top-level query that caused this auditable event. May be more than one statement.';
COMMENT ON COLUMN audit.logged_actions.row_data IS 'Record value. Null for statement-level trigger. For INSERT this is the new tuple. For DELETE and UPDATE it is the old tuple.';
COMMENT ON COLUMN audit.logged_actions.changed_fields IS 'New values of fields changed by UPDATE. Null except for row-level UPDATE events.';
COMMENT ON COLUMN audit.logged_actions.statement_only IS '''t'' if audit event is from an FOR EACH STATEMENT trigger, ''f'' for FOR EACH ROW';

DROP INDEX IF EXISTS audit.logged_actions_relid_idx;
DROP INDEX IF EXISTS audit.logged_actions_action_idx;
CREATE INDEX logged_actions_relid_idx ON audit.logged_actions(relid);
CREATE INDEX logged_actions_action_idx ON audit.logged_actions(action);


CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS TRIGGER AS $BODY$
DECLARE
    audit_row audit.logged_actions;
    include_values boolean;
    log_diffs boolean;
    h_old hstore;
    h_new hstore;
    excluded_cols text[] = ARRAY[]::text[];
	
BEGIN

    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'audit.if_modified_func() may only run as an AFTER trigger';
    END IF;

    audit_row = ROW(
        nextval('audit.logged_actions_id_seq'), 	  -- id
        TG_TABLE_SCHEMA::text,                        -- schema_name
        TG_TABLE_NAME::text,                          -- table_name
        TG_RELID,                                     -- relation OID for much quicker searches
        session_user::text,                           -- session_user_name
        inet_client_addr(),                           -- client_addr
        txid_current(),                               -- transaction ID
        date_trunc('second', current_timestamp),      -- action_tstamp_tx
        date_trunc('second', statement_timestamp()),  -- action_tstamp_stm
        date_trunc('second', clock_timestamp()),      -- action_tstamp_clk
        substring(TG_OP,1,1),                         -- action
        current_query(),                              -- top-level query or queries (if multistatement) from client
        NULL, NULL,                                   -- row_data, changed_fields
        'f'                                           -- statement_only
    );

    IF NOT TG_ARGV[0]::boolean IS DISTINCT FROM 'f'::boolean THEN
        audit_row.query = NULL;
    END IF;

    IF TG_ARGV[1] IS NOT NULL THEN
        excluded_cols = TG_ARGV[1]::text[];
    END IF;
    
    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(OLD.*);
        audit_row.changed_fields = (hstore(NEW.*) - audit_row.row_data) - excluded_cols;
        IF audit_row.changed_fields = hstore('') THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(OLD.*) - excluded_cols;
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(NEW.*) - excluded_cols;
    ELSIF (TG_LEVEL = 'STATEMENT' AND TG_OP IN ('INSERT','UPDATE','DELETE','TRUNCATE')) THEN
        audit_row.statement_only = 't';
    ELSE
        RAISE EXCEPTION '[audit.if_modified_func] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;

    INSERT INTO audit.logged_actions VALUES (audit_row.*);
    RETURN NULL;

END;
$BODY$
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public;


COMMENT ON FUNCTION audit.if_modified_func() IS $BODY$
Track changes to a table at the statement and/or row level.

Optional parameters to trigger in CREATE TRIGGER call:

param 0: boolean, whether to log the query text. Default 't'.

param 1: text[], columns to ignore in updates. Default [].

         Updates to ignored cols are omitted from changed_fields.

         Updates with only ignored cols changed are not inserted into the audit log.

         Almost all the processing work is still done for updates
         that ignored. If you need to save the load, you need to use
         WHEN clause on the trigger instead.

         No warning or error is issued if ignored_cols contains columns
         that do not exist in the target table. This lets you specify
         a standard set of ignored columns.

There is no parameter to disable logging of values. Add this trigger as
a 'FOR EACH STATEMENT' rather than 'FOR EACH ROW' trigger if you do not
want to log row values.

Note that the user name logged is the login role for the session. The audit trigger
cannot obtain the active role because it is reset by the SECURITY DEFINER invocation
of the audit trigger its self.
$BODY$;



CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass, audit_rows boolean, audit_query_text boolean, ignored_cols text[]) RETURNS void AS $BODY$
DECLARE
  stm_targets text = 'INSERT OR UPDATE OR DELETE OR TRUNCATE';
  _q_txt text;
  _ignored_cols_snip text = '';
  
BEGIN

    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_row ON ' || target_table;
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_stm ON ' || target_table;

    IF audit_rows THEN
        IF array_length(ignored_cols,1) > 0 THEN
            _ignored_cols_snip = ', ' || quote_literal(ignored_cols);
        END IF;
        _q_txt = 'CREATE TRIGGER audit_trigger_row AFTER INSERT OR UPDATE OR DELETE ON ' || 
                 target_table || 
                 ' FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func(' ||
                 quote_literal(audit_query_text) || _ignored_cols_snip || ');';
        RAISE NOTICE '%',_q_txt;
        EXECUTE _q_txt;
        stm_targets = 'TRUNCATE';
    ELSE
    END IF;

    _q_txt = 'CREATE TRIGGER audit_trigger_stm AFTER ' || stm_targets || ' ON ' ||
             target_table ||
             ' FOR EACH STATEMENT EXECUTE PROCEDURE audit.if_modified_func('||
             quote_literal(audit_query_text) || ');';
    RAISE NOTICE '%',_q_txt;
    EXECUTE _q_txt;

END;
$BODY$
LANGUAGE 'plpgsql';


COMMENT ON FUNCTION audit.audit_table(regclass, boolean, boolean, text[]) IS $BODY$
Add auditing support to a table.

Arguments:
   target_table:     Table name, schema qualified if not on search_path
   audit_rows:       Record each row change, or only audit at a statement level
   audit_query_text: Record the text of the client query that triggered the audit event?
   ignored_cols:     Columns to exclude from update diffs, ignore updates that change only ignored cols.
$BODY$;


-- Pg doesn't allow variadic calls with 0 params, so provide a wrapper
CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass, audit_rows boolean, audit_query_text boolean) RETURNS void AS $BODY$
SELECT audit.audit_table($1, $2, $3, ARRAY[]::text[]);
$BODY$ LANGUAGE SQL;


-- And provide a convenience call wrapper for the simplest case
-- of row-level logging with no excluded cols and query logging enabled.
CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass) RETURNS void AS $BODY$
SELECT audit.audit_table($1, BOOLEAN 't', BOOLEAN 't');
$BODY$ LANGUAGE 'sql';

COMMENT ON FUNCTION audit.audit_table(regclass) IS $BODY$
Add auditing support to the given table. Row-level changes will be logged with full client query text. No cols are ignored.
$BODY$;


-- Function to audit all tables of selected schema
CREATE OR REPLACE FUNCTION audit.audit_schema(schema_name varchar) RETURNS void AS $BODY$
DECLARE
	table_name text;
    registro  record;
	
BEGIN
  FOR registro IN SELECT * FROM pg_tables WHERE schemaname = schema_name LOOP
	table_name:= schema_name || '.' || quote_ident(registro.tablename);
	PERFORM audit.audit_table(table_name, BOOLEAN 't', BOOLEAN 't');
  END LOOP;
END;
$BODY$
LANGUAGE 'plpgsql';



-- To audit all the tables of the schema, execute:
SELECT audit.audit_schema('data');

