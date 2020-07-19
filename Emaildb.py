import sqlite3

con = sqlite3.connect('Email.sqlite')

cur = con.cursor()

cur.execute('Drop table if  EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)

''')

fname = input("Enter the file name ")

if len(fname) <1 :
    fname ='mbox.txt'

fh = open(fname)

for line in fh:

    if not line.startswith("From"):
        continue
    pieces = line.split()
    email = pieces[1]
    domain = email.find('@')
    org = email[domain +1:len(email)]
    cur.execute('select count from Counts where org = ?' ,(org,))
    row = cur.fetchone()

    if row is None:
        cur.execute(''' INSERT INTO Counts (org,count) VALUES 
        (?,1)''',(org,))
    else:
        cur.execute('''UPDATE Counts SET count = count+1 where org = ?''',(org,))

con.commit()

sqlstat = cur.execute('SELECT * FROM Counts')

for row in sqlstat:
    print(str(row[0]),row[1])
