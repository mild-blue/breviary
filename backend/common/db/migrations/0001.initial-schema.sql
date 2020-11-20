--
-- file: common/db/migrations/0001.initial-schema.sql
--

CREATE TYPE APP_USER_ROLE AS ENUM (
    'ADMIN',
    'SERVICE'
    );

CREATE TABLE app_users
(
    id         BIGSERIAL     NOT NULL,
    username   TEXT          NOT NULL, -- serves as username
    pass_hash  TEXT          NOT NULL,
    role       APP_USER_ROLE NOT NULL,
    created_at TIMESTAMPTZ   NOT NULL,
    updated_at TIMESTAMPTZ   NOT NULL,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT pk_app_users__id PRIMARY KEY (id),
    CONSTRAINT uk_app_users__email UNIQUE (username)
);

-- BEFORE insert function for trigger
CREATE OR REPLACE FUNCTION set_created_at() RETURNS TRIGGER
AS
$BODY$
BEGIN
    new.created_at := now();
    new.updated_at := new.created_at;
    RETURN new;
END;
$BODY$
    LANGUAGE plpgsql;

-- BEFORE update function for trigger
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER
AS
$BODY$
BEGIN
    new.updated_at := now();
    RETURN new;
END;
$BODY$
    LANGUAGE plpgsql;


-- These two scripts must be executed for each newly added table.
DO
$$
    DECLARE
        t TEXT;
    BEGIN
        FOR t IN
            SELECT table_name FROM information_schema.columns WHERE column_name = 'created_at'
            LOOP
                EXECUTE format('CREATE TRIGGER trg_%I_set_created_at
                    BEFORE INSERT ON %I
                    FOR EACH ROW EXECUTE PROCEDURE set_created_at()', t, t);
            END LOOP;
    END;
$$
LANGUAGE plpgsql;

DO
$$
    DECLARE
        t TEXT;
    BEGIN
        FOR t IN
            SELECT table_name FROM information_schema.columns WHERE column_name = 'updated_at'
            LOOP
                EXECUTE format('CREATE TRIGGER trg_%I_set_updated_at
                    BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE PROCEDURE set_updated_at()', t, t);
            END LOOP;
    END;
$$
LANGUAGE plpgsql;

INSERT INTO app_users(id, username, pass_hash, role, created_at, updated_at)
VALUES (1, 'admin', 'admin', 'ADMIN', now(), now())
