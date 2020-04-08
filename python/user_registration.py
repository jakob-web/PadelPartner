from bottle import route, run, template, static_file, request, redirect
from os import listdir
import hashlib, binascii, os
import psycopg2

con = psycopg2.connect( 
    dbname="padel", 
    user="ak1838",
    password="xrqhw4q4",
    host="pgserver.mah.se")

cur = con.cursor()

 
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    print(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    if pwdhash == stored_password:
        print("YES")
    else:
        print("NO")


# TODO HASH FUNCTION
#Register func:
password = input("Lösenord:")
password = hash_password(password)
print(password)

#login func
#make form pwd to hash type
povided_password = input("Lösenord: ")

#rename 'cred' to stored_password
stored_password = password
# remove if password in cred and instead:
verify_password(stored_password,povided_password)




def register():
    """
    Receives User resitration information from a form and creates Person & Profile in the database.
    """

    # data regarding the person table
    förnamn = getattr(request.forms,"fNamn")
    efternamn = getattr(request.forms,"eNamn")
    pnr = getattr(request.forms,"pnr")
    level = getattr(request.forms,"level")
    info = getattr(request.forms,"info")
    print(förnamn, efternamn, pnr, level, info)
    
    # data regarding the profile table
    userName = getattr(request.forms,"userName")
    password = getattr(request.forms,"pwd")
    print(userName, password)
    password = hash_password(password)
    print(password)

    # fetches the current highest id num and adds 1
    cur.execute("select max(id) from profile")
    for row in cur:
        id=row[0]
        id=id+1

    # if user name doesn't already exists
    cur.execute('select username from profile')
    usernameList = cur.fetchall()
    usernameList = ("".join(str(usernameList)))
    print(usernameList)
    if userName not in usernameList:
        print("Yeeey")
    
        def insertPerson():
            sql = "insert into person values(%s,%s,%s,%s)"
            namn = förnamn + " " + efternamn
            val = pnr,namn,level,info
            cur.execute(sql,val)
            con.commit()
            
        def insertProfile():
            sql = "insert into profile values(%s,%s,%s)"
            val = id,userName,password
            cur.execute(sql,val)
            con.commit()

        insertPerson()
        insertProfile()
        return True
    else: 
        return False