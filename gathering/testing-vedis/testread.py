from vedis import Vedis

db = Vedis('testdb.db')

s = db.Set('some set')

print(s.to_set())
counter = 0
db.close()
while 1:
    db.open()
    if (s.peek() != counter):
        print(s.peek())
        counter = s.peek()
    db.close()
