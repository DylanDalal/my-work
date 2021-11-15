# Dylan Dalal
# dmd19e
# 2.16.21
# This work is the individual work of Dylan Dalal.
import sqlite3

conn = sqlite3.connect('reviewData.db')
c = conn.cursor()

try:
    c.execute('''Drop table Reviews''')
    conn.commit()
    print('Reviews table dropped.')
except:
    print('Reviews table did not exist')

try:
    c.execute('''Drop table Ratings''')
    conn.commit()
    print('Ratings table dropped.')
except:
    print('Ratings table did not exist')

c.execute('''CREATE TABLE Reviews(
    Username    VARCHAR(40) NOT NULL,
    Restaurant  VARCHAR(50) NOT NULL,
    ReviewTime  DATETIME NOT NULL, 
    Rating      FLOAT NOT NULL,
    Review      VARCHAR(500) NOT NULL)
''');
conn.commit()

c.execute('''CREATE TABLE Ratings (
    Restaurant  VARCHAR(50) NOT NULL,
    Food        FLOAT NOT NULL,
    Service     FLOAT NOT NULL,
    Ambience    FLOAT NOT NULL,
    Price       FLOAT NOT NULL,
    Rating      FLOAT NOT NULL)
''')

conn.commit()
print('Tables Ratings and Reviews have been created.')

nm = str("Dylan")

for row in c.execute('SELECT * FROM Ratings;'):
    print("fuck")
    print(row)


conn.commit()
print('')

c.close()