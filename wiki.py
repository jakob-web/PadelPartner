from bottle import route, run, template, request, static_file, error
import os 
from os import path
wiki_dir = "wiki"
 
import psycopg2
conn = psycopg2.connect(dbname="ofdagbladet", user="aj9613",password="g0rvfpok",host="pgserver.mah.se")
cursor = conn.cursor() 



def get_articles(): 
    """ 
    Fetches and then returns all the articles in form of a list
    """

    cursor.execute("select rubrik from artikel2 order by datum desc;") #Hämtar artiklarna och ordnar efter datum, nyast högst upp.

    articles = []
    
    for record in cursor:
        articles.append(record[0])
    return articles
    
def get_ingress(): 
    cursor.execute("select ingress from artikel2 order by datum desc;") 

    ingress = []
    
    for record in cursor:
        ingress.append(record[0])
    return ingress

def get_date(): 
    cursor.execute("select datum from artikel2 order by datum desc;") 

    datum = []
    
    for record in cursor:
        datum.append(record[0])
    return datum

def get_author(pagename):
    cursor.execute("select person.namn from ((forfattare join person on forfattare.pnr = person.pnr) join artikel2 on artikel2.artnr = forfattare.artnr) where artikel2.rubrik = %s", [pagename])
    name = []
    
    for record in cursor:
        name.append(record[0])
    name = (",".join(name))
    return name

def get_comments(pagename):
    #DISTINCT användes då varje kommentar oönskat kom upp 5 gånger.
   cursor.execute("select artnr from artikel2 where rubrik = %s", [pagename])
   for row in cursor:
       artnr=row[0]
    
   cursor.execute("select DISTINCT kommentar.knr, kommentar.namn, kommentar.text, date from (kommentar join artikel2 on kommentar.artnr = %s) order by date desc", [artnr])
   comments = []
   for row in cursor:
       knr=str(row[0])
       namn=row[1]
       kommentar=row[2]
       datum=str(row[3])
       h = "ID: " + knr + " Namn:" + namn + " : " + kommentar + ". Datum: " + datum
       comments.append(h)
   return comments

def get_file(pagename):
    """
    Fetches and returns the content (pagename)
    """
    cursor.execute("select text from artikel2 where rubrik=%s", [pagename])
    text = []
    for record in cursor:
        text.append(record[0])

    text = ",".join(text)  
    return text

def get_img(pagename):
    cursor.execute("select artnr from artikel2 where rubrik = %s", [pagename])
    for row in cursor:
       Artnr=row[0]

    cursor.execute("select bilder.link from (bilder join bildText on bilder.bnr = bildText.bnr) where bildText.artnr = %s", [Artnr])
    Img = []
    for record in cursor:
        Img.append(record[0])
    return Img
    
def get_alt(pagename):
    cursor.execute("select artnr from artikel2 where rubrik = %s", [pagename])
    for row in cursor:
       Artnr=row[0]

    cursor.execute("select bilder.alt from (bilder join bildText on bilder.bnr = bildText.bnr) where bildText.artnr = %s", [Artnr])
    Alt = []
    for record in cursor:
        Alt.append(record[0])
    return Alt

def get_imgText(pagename):
    cursor.execute("select artnr from artikel2 where rubrik = %s", [pagename])
    for row in cursor:
       Artnr=row[0]

    cursor.execute("select bildText.text from(bildText join bilder on bildText.bnr = bilder.bnr) where bildText.artnr = %s", [Artnr]) 
    imgText = []
    for record in cursor:
        imgText.append(record[0])
    return imgText

@route("/")
def index():
    """
    This is the home page, which shows a list of links to all articles
    in the database.
    """
    return template("index", articles = get_articles(), ingress = get_ingress(), datum = get_date())


@error(404)
def error404(error):
    """
    Returns a good looking error template with options to go back or create a new article.  
    """
    return template("error")

@route('/wiki/<pagename>/')
def show_article(pagename):
    """ 
    Displays a single article
    """
    return template("article", file = get_file(pagename), pagename = pagename, comments = get_comments(pagename), name = get_author(pagename), links = get_img(pagename), alt = get_alt(pagename), imgText = get_imgText(pagename))
   
@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root="static")


@route('/edit/<pagename>/')
def add_form(pagename):
    """
    Shows a form which allows the user to input a new article.
    """
    return template("edit", file = get_file(pagename), pagename = pagename)
    
@route('/add/')
def edit_form():
    """
    Shows a form which allows the user to add comments for an article.
    """
    return template("add")

@route('/remove/<pagename>')
def remove_form(pagename):
    """
    Shows a form which allows the user to a knr for the comment to be deleted.
    """
    return template("remove", pagename = pagename)

@route('/update/', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates.
    """
    subject = request.forms.get("Titel")
    ing = request.forms.get("Ingress")
    content = request.forms.get("content")
    Författare = request.forms.get("pnr")
    link = request.forms.get("link")
    alt = request.forms.get("alt")
    imgText = request.forms.get("imgText")


    cursor.execute("select max(artnr) from artikel2")
    for row in cursor:
        Artnr=row[0]
        Artnr=Artnr+1

    cursor.execute("select max(bnr) from bilder")
    for row in cursor:
        bnr=row[0]
        bnr=bnr+1

    def writeArticle():
        sql = "insert into artikel2 (artnr,rubrik,Datum,text,ingress) values(%s,%s,%s,%s,%s)"
        
        Rubrik = subject
        Text = content
        ingress = ing
        def Datum():
            cursor.execute("select CURRENT_TIMESTAMP")
            for row in cursor:
                Datum=row[0]
            return Datum   
        val = Artnr, Rubrik, Datum(), Text, ingress
        cursor.execute(sql,val)
        conn.commit()
        def InsertWriter():
            sql = "insert into forfattare values(%s,%s)"
            val = Artnr, Författare
            cursor.execute(sql,val)
            conn.commit()
        InsertWriter()

        def insert_img():
            sql = "insert into bilder values(%s,%s,%s)"
            val = bnr, link, alt
            cursor.execute(sql,val)
            conn.commit()
        insert_img()    


        def insert_imgText():
            sql = "insert into bildText values(%s,%s,%s)"
            val = bnr, Artnr, imgText
            cursor.execute(sql,val)
            conn.commit()
        insert_imgText()
    writeArticle()

    return template("index", articles = get_articles(), ingress = get_ingress(), datum = get_date())


@route('/updateComments/', method="POST")
def update_comments():
    """
    Receives comment information from a form, and creates a comment.
    """
    subject = request.forms.get("Titel")
    Namn = request.forms.get("namn")
    content = request.forms.get("content")
    print(subject)
    def writeComment():
        sql = "insert into kommentar (knr,namn,text,artnr,date) values(%s,%s,%s,%s,%s)"
        cursor.execute("select max(knr) from kommentar")
        for row in cursor:
            knr=row[0]
        knr=knr+1
        namn = Namn
        text = content
        def Datum():
            cursor.execute("select CURRENT_TIMESTAMP")
            for row in cursor:
                Datum=row[0]
            return Datum  
        def artnr():
            cursor.execute("select artnr from artikel2 where rubrik = %s", [subject])
            for row in cursor:
                artnr=row[0]
            return artnr
        val = knr,namn,text,artnr(),Datum()
        cursor.execute(sql,val)
        conn.commit()
    writeComment()
    return template("article", file = get_file(subject), pagename = subject, comments = get_comments(subject), name = get_author(subject))


@route('/remove_update/', method="POST")
def remove_comments():
    """
    Recieves knr information from the form.
    Then deletes the comment with help of that id.
    """
    knr = (request.forms.get("knr"))
    pagename = (request.forms.get("Rubrik"))

    cursor.execute("delete from kommentar where knr = %s", [knr])
    return template("article", file = get_file(pagename), pagename = pagename, comments = get_comments(pagename), name = get_author(pagename))

    
run(host='localhost', port=8080, debug=True, reloader=True)
conn.close()
