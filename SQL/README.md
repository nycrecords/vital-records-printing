#### Before running `run.sh`, ensure the following:

- `standard_conforming_strings = off` in `postgresql.conf`
    - This will allow values with escaped quotes (`\'`) to be inserted
    - An alternative to this would be to change every instance of `\'` to `''` (two single quotes) 
    within the `*_add.sql` files
   
- The directory structure of `SQL/` looks like this:

```
.
├── birth
│   ├── nyc_birth_index_add.sql
│   ├── nyc_birth_index_create.sql
│   └── nyc_birth_index_del.sql
├── death
│   ├── nyc_death_index_add.sql
│   ├── nyc_death_index_create.sql
│   └── nyc_death_index_del.sql
├── marriages
│   ├── nyc_marriages_add.sql
│   ├── nyc_marriages_create.sql
│   └── nyc_marriages_del.sql
└── run.sh
```