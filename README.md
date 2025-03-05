# MSSQL to MySQL Schema Converter

## Overview

This tool helps convert MSSQL schema SQL files into MySQL-compatible schema files. Since direct conversion is complex, we first use [SQL-Hub](https://sql-hub.com/Page/index.php?Shortname=amstomy#mysql) to perform the initial transformation. This tool then cleans up the output from SQL Hub to fix missed conversions and improve compatibility.

## Prerequisites

-   First, convert the MSSQL schema using [SQL-Hub](https://sql-hub.com/Page/index.php?Shortname=amstomy#mysql).
    
-   Modify any necessary expressions in SQL-Hub before exporting the script.
    
-   Use this tool to refine and clean up the output SQL file.
    

## Features

-   Converts MSSQL-specific data types to MySQL equivalents.
    
-   Removes MSSQL-specific syntax (e.g., `SET ANSI_NULLS ON`, `GO` statements, etc.).
    
-   Fixes identifier brackets `[ ]` by converting them to MySQL backticks `` ` ``.
    
-   Handles most datatype conversions automatically.
    

## Limitations & Manual Fixes Required

While this tool automates most of the conversion, some manual adjustments are necessary:

-   **DATETIME and TIME Precision:** SQL Server allows precision greater than 6, which MySQL does not fully support. If the precision is greater than 6, you must manually adjust it.
    
-   **Other Data Types:** Some data types may require trial and error to find the best equivalent in MySQL.
    
-   **ALTER TABLE Statements:** Any `ALTER TABLE` commands from MSSQL may not be fully converted and need manual intervention.
    
-   **VARCHAR Limits:** If MySQL throws a `Row size too large` error, consider changing large `VARCHAR(1000+)` fields to `TEXT`.
    

## Usage

1.  Convert the MSSQL schema using [SQL-Hub](https://sql-hub.com/Page/index.php?Shortname=amstomy#mysql), copy the output from the text area, create an SQL file, and paste the converted script into it.
    
2.  Run the tool to further clean up the SQL file:
    
    ```
    python convert_script.py input_sql_file.sql output_sql_file.sql
    ```
    
3.  Review the output and apply any necessary manual fixes as mentioned above.
    

## Example

```
python convert_sql_file.py mssql_schema.sql mysql_schema.sql
```

This will read `mssql_schema.sql`, convert it, and save the cleaned-up MySQL schema in `mysql_schema.sql`.

## Contributing

Feel free to modify the regular expressions in this script if you need more precise conversions. Contributions and improvements are welcome!
