"""
Lo script consente di ricavare una stringa sql per inserimento in una tabella MYSQL/MARIADB
occorre specificare:
FILE_CSV_TXT:il nome del file di ingresso csv o testo (la prima riga deve contenere i nomi dei campi)
FILE_SQL:il nome del file sql su cui scrivere
TABLENAME: nome della tabella su cui inserire i dati
"""
#INIZIALIZZAZIONE COSTANTI
import os
import sys
import pandas as pd

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
if len(sys.argv) < 4 or len(sys.argv) > 4 :
    print("Insufficiente numero di parametri\nNecessario specificare: file_csv,file_sql,nometabella")
    exit()
FILE_CSV_TXT = sys.argv[1] 
FILE_SQL=sys.argv[2] 
DATA_FILE=os.path.join(BASE_DIR,FILE_CSV_TXT)
TABLENAME=sys.argv[3] 

def infer_sql_type(series, column_name):
    """Tries to infer the most appropriate SQL data type for a pandas Series."""
    if series.empty:
        return "TEXT"  # Default to TEXT if the column is empty

    if pd.api.types.is_integer_dtype(series):
        # Check for potential overflow with larger integers
        if series.max() > 2147483647 or series.min() < -2147483648:
            return "BIGINT"
        else:
            return "INT"
    elif pd.api.types.is_float_dtype(series):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    elif series.astype(str).str.match(r'^(true|false)$', case=False).all():
        return "BOOLEAN"
    else:
        
        return "VARCHAR(100)"

def get_sql_from_csv(f,header=True,separator=","):
    """
    input f:file csv
          header: True/False
          separtaror: character to separate fields in csv file
    output:string (sql insert)      
    """
   
    if (header):
        fields=f.readline().rstrip()
        
    df=pd.read_csv(FILE_CSV_TXT,delimiter=separator)#,dtype={"ZIP":str})
    dict_types={}
    for col_name in df.columns:
        dict_types[col_name]=infer_sql_type(df[col_name],col_name)
    print(dict_types)    
    col_types=[infer_sql_type(df[col_name],col_name) for col_name in df.columns]
    print(col_types)
    #ciclo sulle righe 
    sqlInsert="INSERT INTO "+TABLENAME+ " VALUES "
    for item in f:
        if item.rstrip()!="":
            sql_values=""
            row_values=item.split(separator)
            for col_type,value in zip(col_types,row_values):
                
                if "VARCHAR" in col_type:
                    sql_values+='"'+value+'",'
                elif value is None:
                    sql_values+="NULL,"  
                else:
                    sql_values+=value+","    
        sqlInsert+="\n(" +sql_values[:-1]+"),"  
    sqlInsert=sqlInsert.replace(",,",",NULL,")
    return sqlInsert[:-1]+";"

if not (os.path.exists(DATA_FILE)):
    print("File:",DATA_FILE, " non esiste!")
    exit()

#open the file file and retrieve the list of CF
with open(DATA_FILE) as f:
    #print f.readline()
    sqlInsert=get_sql_from_csv(f,header=True,separator=",")     

with open(FILE_SQL,"w") as f:
    f.write(sqlInsert)    

#print(sqlInsert)    

    
