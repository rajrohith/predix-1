DROP TABLE IF EXISTS public.temp_factjobdetail;
CREATE TABLE public.temp_factjobdetail(
    dr_loadtime timestamp(6) without time zone NOT NULL,
    dr_recordtime timestamp(6) without time zone NOT NULL,
    fk_date integer NOT NULL,
    fk_drwell integer NOT NULL,
    fk_disclosure integer NOT NULL,
    fk_supplier integer NOT NULL,
    fk_trade integer NOT NULL,
    fk_ingredient integer NOT NULL,
    fk_purpose integer NOT NULL,
    purposematchconfidence numeric(10, 2),
    purposematchingstrategy character varying(36) COLLATE pg_catalog."default",
    ingredientmatchconfidence double precision,
    ingredientmatchingstrategy character varying(21) COLLATE pg_catalog."default",
    percenthighadditive double precision,
    ingredienthfjobpercent numeric(22, 12),
    calcingredientmass numeric(18, 4),
    ingredientmassuom character varying(2) COLLATE pg_catalog."default" NOT NULL
);
commit;
SET client_encoding = 'ISO_8859_5';
