# csv2create
It generates an sql statement to create a table based on a csv/txt file.
The column name and types are inferred by the header of the csv/txt file.
You should verify and add necessary constraints.

The syntax to launch the script is:
python csv2create.py [csv filename] [ouput file (sql)] [nome tabella]


# csv2sql
It generates an sql statement to insert values in a table based on a csv/txt file.
The column name are inferred by the header of the csv/txt file.

The syntax to launch the script is:
python csv2sql.py [csv filename] [ouput file (sql)] [nome tabella]
