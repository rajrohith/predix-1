DROP TABLE IF EXISTS public.temp_dimdiwellheadermaster;
CREATE TABLE public.temp_dimdiwellheadermaster(
    dr_id integer NOT NULL DEFAULT ,
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_start timestamp(6) without time zone NOT NULL,
    dr_end timestamp(6) without time zone NOT NULL,
    dr_current boolean NOT NULL,
    drwellid integer NOT NULL,
    wellgovtid character varying(30) COLLATE pg_catalog."default",
    api character varying(30) COLLATE pg_catalog."default",
    wellname text COLLATE pg_catalog."default" NOT NULL,
    countryname character varying(100) COLLATE pg_catalog."default",
    statename character varying(100) COLLATE pg_catalog."default" NOT NULL,
    countyname character varying(100) COLLATE pg_catalog."default" NOT NULL,
    drillingoperator character varying(255) COLLATE pg_catalog."default",
    aliaseddrillingoperator character varying(255) COLLATE pg_catalog."default",
    firstspuddate timestamp(3) without time zone,
    md integer,
    mduom character varying(10) COLLATE pg_catalog."default",
    tvd integer,
    fftvd integer,
    tvduom character varying(10) COLLATE pg_catalog."default",
    surfacelatitude numeric(14, 9),
    surfacelongtitude numeric(14, 9),
    projection text COLLATE pg_catalog."default" NOT NULL,
    sysmodifieddate timestamp(3) without time zone,
    matchingresult text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT dimdiwellheadermaster_pkey PRIMARY KEY (dr_id)
);
commit;
SET client_encoding = 'ISO_8859_5';
