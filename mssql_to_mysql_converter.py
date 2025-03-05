import re
#import sys #debugging purpose

#print("\033[31mCheck code first before execute\033[0m")  # Red
#sys.exit()  # Stops execution

def convert_mssql_to_mysql(schema):
    """
    Converts MSSQL schema to MySQL-compatible schema.
    """
    type_mapping = {
        r'(?i)INT IDENTITY\(\d+,\d+\)': 'INT AUTO_INCREMENT',
        r'(?i)DATETIME2': 'DATETIME',
        r'(?i)DATETIMEOFFSET': 'DATETIME',
        r'(?i)SMALLDATETIME': 'DATETIME',
        r'(?i)DATETIME\(7\)': 'DATETIME(6)',
        r'(?i)TIME\(7\)': 'TIME(6)',
        r'(?i)UNIQUEIDENTIFIER': 'VARCHAR(36)',
        r'(?i)NVARCHAR\((\d+)\)': r'VARCHAR(\1)',
        r'(?i)NVARCHAR\(MAX\)': 'TEXT',
        r'(?i)VARCHAR\(MAX\)': 'TEXT',
        r'(?i)TEXT': 'LONGTEXT',
        r'(?i)NTEXT': 'LONGTEXT',
        r'(?i)MONEY': 'DECIMAL(19,4)',
        r'(?i)SMALLMONEY': 'DECIMAL(10,4)',
        r'(?i)BIT': 'TINYINT(1)',
        r'(?i)FLOAT': 'DOUBLE',
        r'(?i)REAL': 'FLOAT',
        r'(?i)TINYINT': 'TINYINT UNSIGNED',
        r'(?i)BIGINT': 'BIGINT',
        r'(?i)IMAGE': 'LONGBLOB',
    }
    
    for pattern, replacement in type_mapping.items():
        schema = re.sub(pattern, replacement, schema, flags=re.IGNORECASE)
    
    # Ensure all DATETIME and TIME with precision greater than 6 are converted to DATETIME(6) and TIME(6)
    schema = re.sub(r'(?i)DATETIME\(\d+\)', 'DATETIME(6)', schema)
    schema = re.sub(r'(?i)TIME\(\d+\)', 'TIME(6)', schema)
    
    # Remove MSSQL-specific settings
    schema = re.sub(r'(?i)SET ANSI_NULLS ON;?', '', schema)
    schema = re.sub(r'(?i)SET QUOTED_IDENTIFIER ON;?', '', schema)
    
    # MSSQL uses [schema].[table] notation, remove it for MySQL
    schema = re.sub(r'\[dbo\]\.\[?(\w+)\]?', r'`\1`', schema)
    
    # Convert bracketed identifiers to backticks
    schema = re.sub(r'\[(.*?)\]', r'`\1`', schema)
    
    # Remove extra backticks around TINYINT UNSIGNED
    schema = re.sub(r'`(TINYINT UNSIGNED)`', r'\1', schema)
    
    # Remove backticks around data types in column definitions
    schema = re.sub(r'`(\w+)`\s+`(\w+)`', r'`\1` \2', schema)
    
    # Convert GO statements to MySQL-compatible
    schema = re.sub(r'(?i)^GO\s*$', '', schema, flags=re.MULTILINE)
    
    return schema

def read_file_with_encoding(file_path):
    """
    Tries to read a file with multiple encodings to handle different formats.
    """
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("None of the tested encodings worked for this file.")

def convert_sql_file(input_file, output_file):
    """
    Reads an MSSQL SQL file, converts it, and writes the MySQL SQL file.
    """
    mssql_schema = read_file_with_encoding(input_file)
    mysql_schema = convert_mssql_to_mysql(mssql_schema)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mysql_schema)
    
    print(f"Converted schema saved to {output_file}")
    print()
    print("The max value for 'datetime' and 'time' data types must be updated manually, as regex cannot handle it automatically.")
    print()
    print("If you encounter the error 'Row size too large', it may be due to VARCHAR(1000) columns. Consider changing them to TEXT in the affected table.")
    print()
    print("MSSQL ALTER TABLE commands may not be fully converted. Review and manually adjust them to proper MySQL syntax where needed.")

# Example Usage
# input_sql_file = 'mssql_schema.sql'
input_sql_file = 'sql_hub_mysql.sql'
output_sql_file = 'mysql_schema.sql'
convert_sql_file(input_sql_file, output_sql_file)
