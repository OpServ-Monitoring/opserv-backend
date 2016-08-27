from vedis import Vedis
import time

db = Vedis('testdb.db')

s = db.Set('some set')

currentTime = time.time()
counter = 0
db.close()
while 1:
    if time.time() - currentTime > 0.5:
        currentTime = time.time()
        
        db.open();
        s.add(counter)
        db.close();
        counter += 1
