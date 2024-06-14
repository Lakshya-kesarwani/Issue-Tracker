from flask import Flask,render_template,jsonify,request,redirect,url_for,flash
from sqlalchemy import text,Column,Integer,String,Boolean,Text
from databse import engine, load_admin_details,load_queries
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app=Flask(__name__)
app.secret_key ="lk_8517"
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)
    issue = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_link = Column(String(255))
    is_open = Column(Boolean, default=True)

    def __repr__(self):
        return f'<Issue {self.name}>'
@app.route("/")
def home_page():
    return render_template("home-page.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/new")
def new_query():
    return render_template("query.html")

@app.route("/new",methods=["GET","POST"])
def fill_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        subject = request.form['subject']
        description = request.form['issue']
        link = request.form['link']

        with engine.connect() as conn:
            query = text("INSERT INTO issues (name,email,mobile,issue,description,image_link) VALUES (:name,:email,:number,:subject,:description,:link)")
            values ={"name":name,"email":email,"number":number,"subject":subject,"description":description,"link":link}
            # values =[name,email,number,subject,description,link]
            conn.execute(query,values)
            conn.commit()
        flash('Issue submitted successfully!', 'success')
    return (render_template("query.html"))
        
@app.route("/admin",methods=["GET","post"])
def login_to_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # with engine.connect() as conn:
        #     query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        #     values = (username, password)
        #     res = conn.execute(query, values)
        #     result = res.fetchone()
        tup = {"username":username,"password":password}
        data_db = load_admin_details()

        if tup in data_db:
            flash('Login successful!', 'success')
            # Redirect to the desired page after successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template("admin.html")
    
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    # Code for the dashboard page goes here
    session = Session()
    issues = session.query(Issue).all()
    session.close()

    if request.method == 'POST':
        issue_id = request.form.get('issue_id')

        if issue_id:
            session = Session()
            issue = session.query(Issue).get(issue_id)

            if issue:
                issue.is_open = not issue.is_open  # Toggle the is_open value
                session.commit()


        session.close()

        return redirect(url_for('dashboard'))

    return render_template('list.html', issues=issues)

@app.route('/exist', methods=['GET', 'POST'])
def query_status():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        session = Session()
        user_issues = session.query(Issue).filter(Issue.name == name, Issue.mobile == mobile).all()
        session.close()

        return render_template('query_status.html', user_issues=user_issues)

    return render_template('query_status.html')

if __name__=="__main__":
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0',debug= True)
