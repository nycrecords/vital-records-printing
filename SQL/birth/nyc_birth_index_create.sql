-- Exported from MS Access to PostgreSQL
-- (C) 1997-98 CYNERGI - www.cynergi.net, info@cynergi.net

CREATE TABLE NYC_Births_1901_190
     (
     ID                    serial,
     Surname              varchar(25),
     GivenName            varchar(25),
     Month                varchar(3),
     Day                  varchar(6),
     Year                 varchar(4),
     County               varchar(10),
     CertNbr              varchar(10),
     Soundex              varchar(4)
     );

