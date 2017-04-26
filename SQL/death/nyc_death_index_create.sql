-- Exported from MS Access to PostgreSQL
-- (C) 1997-98 CYNERGI - www.cynergi.net, info@cynergi.net

CREATE TABLE _1868_1890_Deaths_M
     (
     Error                varchar(255),
     Field                varchar(255),
     Row                  int8
     );


CREATE TABLE _1868_1890_Deaths_Ma -- 1868_1890_Deaths_Ma
     (
     Surname              varchar(30),
     GivenName            varchar(50),
     Age                  varchar(10),
     Month                varchar(3),
     Day                  varchar(10),
     Year                 varchar(4),
     CertNbr              varchar(10),
     County               varchar(10),
     Soundex              varchar(4)
     );


CREATE TABLE Jrs -- Jr's
     (
     Surname              varchar(30),
     GivenName            varchar(50),
     Age                  varchar(10),
     Month                varchar(3),
     Day                  varchar(10),
     Year                 varchar(4),
     CertNbr              varchar(10),
     County               varchar(10),
     Soundex              varchar(4)
     );


CREATE TABLE Totals
     (
     Field1               varchar(50),
     Field2               int8,
     Field3               int8
     );
