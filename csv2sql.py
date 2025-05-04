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

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
if len(sys.argv) < 4 or len(sys.argv) > 4 :
    print("Insufficiente numero di parametri\nNecessario specificare: file_csv,file_sql,nometabella")
    exit()
FILE_CSV_TXT = sys.argv[1] 
FILE_SQL=sys.argv[2] 
DATA_FILE=os.path.join(BASE_DIR,FILE_CSV_TXT)
TABLENAME=sys.argv[3] 

def get_sql_from_csv(f,header=True,separator=","):
    """
    input f:file csv
          header: True/False
          separtaror: character to separate fields in csv file
    output:string (sql insert)      
    """
   
    if (header):
        fields=f.readline().rstrip()
        
    #ciclo sulle righe 
    sqlInsert="INSERT INTO "+TABLENAME+ "(" + fields + ") VALUES "
    for item in f:
        if item.rstrip()!="":
            sqlInsert+="\n(" +item.rstrip()+"),"  

    return sqlInsert[:-1]

if not (os.path.exists(DATA_FILE)):
    print("File:",DATA_FILE, " non esiste!")
    exit()

#open the file file and retrieve the list of CF
with open(DATA_FILE) as f:
    #print f.readline()
    sqlInsert=get_sql_from_csv(f,header=True,separator=",")     

with open(FILE_SQL,"w") as f:
    f.write(sqlInsert)    

print(sqlInsert)    

    
