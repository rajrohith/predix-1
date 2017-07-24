DORP TABLE IF EXISTS public.temp_topingredientsusedforeachpurpose;
CREATE TABLE public.temp_topingredientsusedforeachpurpose(
	PurposeName Text NULL,
	CasNumber Varchar(100) NOT NULL,
	IngredientName Varchar(300) NOT NULL,
	NoofOccurance int NULL,
	rank_IngredientName bigint NULL
);
commit;
SET client_encoding = 'ISO_8859_5';
