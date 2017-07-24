CREATE TEMP TABLE IF NOT EXISTS dimsupplier(
    dr_id integer NOT NULL,
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_start timestamp(6) without time zone NOT NULL,
    dr_end timestamp(6) without time zone NOT NULL,
    dr_current boolean NOT NULL,
    suppliername text COLLATE pg_catalog."default",
    suppliercategory text COLLATE pg_catalog."default",
    CONSTRAINT dimsupplier_pkey PRIMARY KEY (dr_id)
);