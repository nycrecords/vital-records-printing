-- Exported from MS Access to PostgreSQL
-- (C) 1997-98 CYNERGI - www.cynergi.net, info@cynergi.net

CREATE TABLE Brides_1866_1900
     (
     ID                    serial,
     Surname              varchar(35),
     GivenName            varchar(50),
     Month                varchar(3),
     Day                  varchar(6),
     Year                 varchar(4),
     CertNbr              varchar(6),
     County               varchar(10),
     Soundex              varchar(4)
     );


CREATE TABLE Grooms_1866_1900
     (
     ID                    serial,
     Surname              varchar(35),
     GivenName            varchar(50),
     Month                varchar(3),
     Day                  varchar(6),
     Year                 varchar(4),
     CertNbr              varchar(6),
     County               varchar(10),
     Soundex              varchar(4)
     );


-- CREATE TABLE Totals
--      (
--      Field1               varchar(50),
--      Field3               int8,
--      County               varchar(50),
--      Count                int8 DEFAULT 0
--      );

