CREATE TABLE IF NOT EXISTS dimdisclosure(
    dr_id integer NOT NULL,
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_start timestamp(6) without time zone NOT NULL,
    dr_end timestamp(6) without time zone NOT NULL,
    dr_current boolean NOT NULL,
    jobstartdate timestamp(0) without time zone,
    jobenddate timestamp(0) without time zone,
    ffapi14 character varying(14) COLLATE pg_catalog."default" NOT NULL,
    fracoperator character varying(55) COLLATE pg_catalog."default",
    ffversion real,
    CONSTRAINT dimdisclosure_pkey PRIMARY KEY (dr_id)
);
