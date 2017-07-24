CREATE TEMP TABLE IF NOT EXISTS public.dimtrade(
    dr_id integer NOT NULL,
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_start timestamp(6) without time zone NOT NULL,
    dr_end timestamp(6) without time zone NOT NULL,
    dr_current boolean NOT NULL,
    tradename text COLLATE pg_catalog."default",
    issand character varying(1) COLLATE pg_catalog."default",
    sandmeshsize character varying(20) COLLATE pg_catalog."default",
    sandquality character varying(20) COLLATE pg_catalog."default",
    isresincoated character varying(1) COLLATE pg_catalog."default",
    isartificial character varying(1) COLLATE pg_catalog."default",
    CONSTRAINT dimtrade_pkey PRIMARY KEY (dr_id)
);