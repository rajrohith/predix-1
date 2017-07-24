DROP TABLE IF EXISTS public.temp_factdisclosuredetail;
CREATE TABLE public.temp_factdisclosuredetail(
"dr_loadtime" timestamp  with time zone NOT NULL,
 "dr_recordTime" timestamp with time zone NOT NULL,
 "fk_disclosure" integer NOT NULL,
"fk_drweell" integer NOT NULL,
 "totalbasewatervolume" numeric(18, 2) NULL,
"totalbasewatervolumeuom" character varying(3)  NULL,
"totalbasenonwatervolume" numeric(18, 2) NULL,
 "totalbasenonwatervolumeuom" character varying(3) NULL ,
"parsedwaterdensity" numeric(10, 2) NULL,
 "parsedwaterdensityuom" character varying(3)  NOT NULL,
 "calctotalwatermass" numeric(18, 2) NULL,
 "calctotalwatermassuom" character varying(5)  NULL,
"hfjobWaterpercent" numeric(22, 2) NULL,
"calctotalmass" numeric(18, 2) NULL,
"calctotalmassuom" character varying(5)  NULL,
"calcTotalingredientmass" numeric(19, 2) NULL,
"calcTotalingredientmassuom" character varying(5)  NULL
);
commit;
SET client_encoding = 'ISO_8859_5';
