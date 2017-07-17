DROP TABLE IF EXISTS public.temp_date;
CREATE TABLE  public.temp_date(
                DR_ID int NOT NULL primary key,
                DR_LoadTime Timestamp(6) NOT NULL,
                FullDate Timestamp(6) NULL,
                Year int NULL,
                Quarter Varchar(100) NULL,
                Quarter_of_Year int NULL,
                Month Varchar(100) NULL,
                Month_of_Year int NULL,
                Week Varchar(100) NULL,
                Week_of_Year int NULL,
                Day Varchar(100) NULL,
                Day_of_Week int NULL,
                Day_of_Month int NULL,
                Day_of_Year int NULL,
                Time_Hour_24 int NULL,
                Time_Minute int NULL,
                Time_24 Varchar(100) NULL,
                Date Varchar(100) NULL,
                Date_ANSI Varchar(100) NULL,
                Date_USA Varchar(100) NULL,
                Date_British Varchar(100) NULL,
                Date_German Varchar(100) NULL,
                Date_Italian Varchar(100) NULL,
                Date_String Varchar(100) NULL,
                DateTime_ODBC Varchar(100) NULL
);
 commit;  
SET client_encoding = 'ISO_8859_5';
COPY public.temp_date FROM '/app/dbdata/Date_Table.txt' DELIMITER '|' NULL AS ''  CSV HEADER;
commit;
DROP TABLE IF EXISTS public.date;
commit;
ALTER TABLE temp_date RENAME TO date;
commit;
