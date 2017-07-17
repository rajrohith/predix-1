CREATE TEMP TABLE IF NOT EXISTS dimpurpose
(
    dr_id integer NOT NULL,
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_start timestamp(6) without time zone NOT NULL,
    dr_end timestamp(6) without time zone NOT NULL,
    dr_current boolean NOT NULL,
    purposename text COLLATE pg_catalog."default",
    purposedescription text COLLATE pg_catalog."default",
    CONSTRAINT dimpurpose_pkey PRIMARY KEY (dr_id)
)