# CALCPRAZO
Calc prazo is FREE and simple date calculator aimed to be used by local lawyers and legal assistents for daly deadline calculation.

The calculator was first created as a spreadsheet publicaly shered via gogle drive.

The present project is a migration to a Django Application open source free for general use, as a tool for quickly calculate legal deadlines.

## Funcionality.
### INPUTs
1st User inputs a start date, or date 0 (zero).  
2nd User inputs the (+) plus or (-) minus delta days to calculate the DEADLINE. 

### OUTPUTs
App will calculate and return 3 (three) results:

1. DEADLINE calculated in simple Delta days.
Example: March,1,2022(Tue) + 7 days = March,7,2022(Mon)

2. DEADLINE WORKDAY calculated computing only workdays, accounting for SATURDAYS, SUNDAYS and for World Wide (Brazil) holidays. Table Feriado dates flagged with "F".
March,1,2022(Tue) + 7 days = March,10,2022(Thu)

3. DEADLINE WORKDAY SPECIAL calculated accounting for all entries in table Feriado ('F', 'P', 'I')


## User Return Information
The result will be returned to the user in a html page, presenting all user inputs, a summary of the 3 output calculations.

Result page also must present the calculation demonstration for the 3rd result, presenting all dates disregarded as non-working date.


# Reference Spreadsheet
As more detailed explanations for the calculations, a reference spreadsheet is available at [google drive - CALCULADORA DE PRAZOS TJSP](https://docs.google.com/spreadsheets/d/1-x3NV5LPIvQ-dC5jwjpuF3e_jrVeC4W4cWU5fQdNOJk/edit?usp=sharing)



## Login Information
User loggin information will be kept as minimum as possible.
A history table will logg all calculations with a timestamp and user email
User email information is optional, but will help user as the Calculation Demonstration will be able to be send a copy to the email.



1. Perform migrations: 

    python manage.py makemigrations

    Or Do the migrations separately in case the command does not fail.

    python manage.py makemigrations calcprazo


    And finally create the database.

    python manage.py migrate


3. Run the project:

    python manage.py runserver

Load test data (Optional):

* In Local:

    python manage.py loaddata calcprazo/data/users.json

    python manage.py loaddata calcprazo/data/feriados.json


* Admin information

    email: admin@gmail.com
    
    password: admin!@#

