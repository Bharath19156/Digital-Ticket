from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, send_file
from pymongo import MongoClient
import bcrypt  # For password hashing
import pprint
from werkzeug.utils import secure_filename
import os
import gridfs
from bson.objectid import ObjectId
from flask import Response
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import qrcode
import io
from PIL import Image





app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["digital_ticket"]
fs = gridfs.GridFS(db)
collection = db["signup_data"]
collection_generalBusPass=db["generalBusPass_details"]
collection_generalMetroPass=db["generalMetroPass_details"]
collection_studentBusPass=db['studentBusPass_details']
collection_studentMetroPass=db['studentMetroPass_details']
collection_conductor=db['conductor_deatils']
collection_fare=db['fare_prices']





@app.route('/photo/<photo_id>')
def get_photo(photo_id):
    try:
        print(f"Requesting photo with ID: {photo_id}")
        file = fs.get(ObjectId(photo_id))
        return Response(file.read(), mimetype=file.content_type)
    except Exception as e:
        print(f"Photo loading error for ID {photo_id}: {e}")
        return "Image not found", 404



UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # full path to uploads/

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    fare_data=list(collection_fare.find())
    return render_template('index.html',fare_data=fare_data)

@app.route('/user')
def user():
    return render_template('signup.html', role="user")

@app.route('/conductor')
def conductor():
    return render_template('signup.html', role="conductor")

@app.route('/admin')
def admin():
    return render_template('signup.html', role="admin")

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")  # Raw password
    role = request.form.get("role")

    if not all([name, email, password, role]):
        flash("All fields are required!", 'danger')
        return redirect(url_for('signup'))

    # Hash the password before saving it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role
    }

    collection.insert_one(user_data)
    flash("Signup successful! Please login.", 'success')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    data=""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = collection.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']

            if user['role'] == "admin":
                return redirect(url_for('admin_login'))
            elif user['role'] == "conductor":
                return redirect(url_for('conductor_login'))
            else:
                return redirect(url_for('user_login'))

        flash("Invalid email or password", 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')



#-------------------------------------------------------------------------
#------------------------------User Page----------------------------------
#-------------------------------------------------------------------------


@app.route('/user_login')
def user_login():
    return render_template('user_login.html', message="Hi, welcome back!",email=session.get('email'),name=session.get('user'),role=session.get('role'))



#Funtions to deal with the Genral Bus Passes

def datafrom_generalPassBusForm():
    data={}
    name=request.form['name']
    data['name']=name
    gaurdian_name=request.form['gaurdian_name']
    data['gaurdian_name']=gaurdian_name
    dob=request.form['dob']
    data['dob']=dob
    aadhar_no=request.form['aadhar_no']
    data['aadhar_no']=aadhar_no
    email=request.form['email']
    data['email']=email
    district=request.form['district']
    data['district']=district
    payment_mode=request.form['payment_mode']
    data['payment_mode']=payment_mode
    pass_type=request.form['pass_type']
    data['pass_type']=pass_type
    gender=request.form['gender']
    data['gender']=gender
    user_email=session.get('email')
    user_name=session.get('user')
    role=session.get('role')
    photo = request.files.get('photo')
    if photo:
        file_id = fs.put(photo, filename=photo.filename, content_type=photo.content_type)
        print("Uploaded photo ID:", file_id)
        data['photo'] = file_id
    data["user_email"]=user_email
    data['user_name']=user_name
    data['role']=role
    pprint.pprint(photo)
    return data
@app.route('/generalBusPassForm',methods=['POST', 'GET'] )
def generalBusPassForm():
    data={}
    if request.method == 'POST':
        data=datafrom_generalPassBusForm()
    pprint.pprint(data)
    data['status']='pending'
    data['type_of_pass']='Bus'
    data['type_of_user']='General'
    collection_generalBusPass.insert_one(data)
    return redirect(url_for('user_login'))

#Funtions to deal with the Genral Metro Passes

def datafrom_generalPassMetroForm():
    data={}
    name=request.form['name']
    data['name']=name
    gaurdian_name=request.form['gaurdian_name']
    data['gaurdian_name']=gaurdian_name
    dob=request.form['dob']
    data['dob']=dob
    aadhar_no=request.form['aadhar_no']
    data['aadhar_no']=aadhar_no
    email=request.form['email']
    data['email']=email
    district=request.form['district']
    data['district']=district
    payment_mode=request.form['payment_mode']
    data['payment_mode']=payment_mode
    pass_type=request.form['pass_type']
    data['pass_type']=pass_type
    gender=request.form['gender']
    data['gender']=gender
    user_email=session.get('email')
    user_name=session.get('user')
    role=session.get('role')
    photo = request.files.get('photo')
    if photo:
        file_id = fs.put(photo, filename=photo.filename, content_type=photo.content_type)
        print("Uploaded photo ID:", file_id)
        data['photo'] = file_id
    data["user_email"]=user_email
    data['user_name']=user_name
    data['role']=role
    return data
@app.route('/generalMetroPassForm',methods=['POST', 'GET'] )
def generalMetroPassForm():
    data={}
    if request.method == 'POST':
        data=datafrom_generalPassMetroForm()
    pprint.pprint(data)
    data['status']='pending'
    data['type_of_pass']='Metro'
    data['type_of_user']='General'
    collection_generalMetroPass.insert_one(data)
    return redirect(url_for('user_login'))

#Functions to deal with the Student Bus Passes

def datafrom_studentPassBusForm():
    data = {}

    # 1. SSC Details
    data['ssc_type'] = request.form['ssc_type']
    data['ssc'] = request.form['ssc']
    data['ssc_pass_year'] = request.form['ssc_pass_year']
    data['ssc_hall'] = request.form['ssc_hall']
    data['dob'] = request.form['dob']

    # 2. Student Details
    data['name'] = request.form['name']
    data['gaurdian_name'] = request.form['gaurdian_name']
    data['gender'] = request.form['gender']
    data['aadhar_no'] = request.form['aadhar_no']
    data['WhatsApp_no'] = request.form['WhatsApp_no']
    data['email'] = request.form.get('email', '')
    data['employee'] = request.form['employee']

    # 2.9 Upload Photo
    photo = request.files.get('photo')
    if photo:
        file_id = fs.put(photo, filename=photo.filename, content_type=photo.content_type)
        print("Uploaded photo ID:", file_id)
        data['photo'] = str(file_id)

    # 3. Residential Address
    data['district'] = request.form['district']
    data['mandal'] = request.form['mandal']
    data['village'] = request.form['village']
    data['address'] = request.form['address']
    data['postal_code'] = request.form['postal_code']

    # 4. Institution Details
    data['institution_district'] = request.form['institution_district']
    data['institution_mandal'] = request.form['institution_mandal']
    data['institution_name'] = request.form['institution_name']
    data['course_name'] = request.form['course_name']
    data['admission_no'] = request.form['admission_no']
    data['institution_address'] = request.form['institution_address']

    # 4.7 Upload College ID Photo
    id_photo = request.files.get('id_photo')
    if id_photo:
        id_file_id = fs.put(id_photo, filename=id_photo.filename, content_type=id_photo.content_type)
        print("Uploaded ID Photo ID:", id_file_id)
        data['id_photo'] = str(id_file_id)

    # 5. Payment Mode
    data['payment_mode'] = request.form['payment_mode']

    # 6. Pass Type
    data['pass_type'] = request.form['pass_type']
    #role details
    user_email=session.get('email')
    user_name=session.get('user')
    role=session.get('role')
    data["user_email"]=user_email
    data['user_name']=user_name
    data['role']=role

    return data
@app.route('/studentBusPassForm',methods=['POST', 'GET'] )
def studentBusPassForm():
    data={}
    if request.method == 'POST':
        data=datafrom_studentPassBusForm()
    pprint.pprint(data)
    data['status']='pending'
    data['type_of_pass']='Bus'
    data['type_of_user']='Student'
    pprint.pprint(data)
    collection_studentBusPass.insert_one(data)
    return redirect(url_for('user_login'))


#functions to deal with the Student Metro passes

def datafrom_studentPassMetroForm():
    data = {}

    # 1. SSC Details
    data['ssc_type'] = request.form['ssc_type']
    data['ssc'] = request.form['ssc']
    data['ssc_pass_year'] = request.form['ssc_pass_year']
    data['ssc_hall'] = request.form['ssc_hall']
    data['dob'] = request.form['dob']

    # 2. Student Details
    data['name'] = request.form['name']
    data['gaurdian_name'] = request.form['gaurdian_name']
    data['gender'] = request.form['gender']
    data['aadhar_no'] = request.form['aadhar_no']
    data['WhatsApp_no'] = request.form['WhatsApp_no']
    data['email'] = request.form.get('email', '')
    data['employee'] = request.form['employee']

    # 2.9 Upload Photo
    photo = request.files.get('photo')
    if photo:
        file_id = fs.put(photo, filename=photo.filename, content_type=photo.content_type)
        print("Uploaded photo ID:", file_id)
        data['photo'] = str(file_id)

    # 3. Residential Address
    data['district'] = request.form['district']
    data['mandal'] = request.form['mandal']
    data['village'] = request.form['village']
    data['address'] = request.form['address']
    data['postal_code'] = request.form['postal_code']

    # 4. Institution Details
    data['institution_district'] = request.form['institution_district']
    data['institution_mandal'] = request.form['institution_mandal']
    data['institution_name'] = request.form['institution_name']
    data['course_name'] = request.form['course_name']
    data['admission_no'] = request.form['admission_no']
    data['institution_address'] = request.form['institution_address']

    # 4.7 Upload College ID Photo
    id_photo = request.files.get('id_photo')
    if id_photo:
        id_file_id = fs.put(id_photo, filename=id_photo.filename, content_type=id_photo.content_type)
        print("Uploaded ID Photo ID:", id_file_id)
        data['id_photo'] = str(id_file_id)

    # 5. Payment Mode
    data['payment_mode'] = request.form['payment_mode']

    # 6. Pass Type
    data['pass_type'] = request.form['pass_type']
    #role details
    user_email=session.get('email')
    user_name=session.get('user')
    role=session.get('role')
    data["user_email"]=user_email
    data['user_name']=user_name
    data['role']=role

    return data
@app.route('/studentMetroPassForm',methods=['POST', 'GET'] )
def studentMetroPassForm():
    data={}
    if request.method == 'POST':
        data=datafrom_studentPassMetroForm()
    pprint.pprint(data)
    data['status']='pending'
    data['type_of_pass']='Metro'
    data['type_of_user']='Student'
    pprint.pprint(data)
    collection_studentMetroPass.insert_one(data)
    return redirect(url_for('user_login'))

#funtion to display the transactions made

@app.route('/user_login/view_transactions/<role>/<name>/<email>')
def view_transactions(role, name, email):
    datafrom_generalPassBusForm=[]
    datafrom_generalPassMetroForm=[]
    datafrom_studentPassBusForm=[]
    datafrom_studentMetroBusForm=[]
    query = {"user_name": name, "user_email": email, "role": role}
    if list(collection_generalBusPass.find(query)):
        datafrom_generalPassBusForm = list(collection_generalBusPass.find(query))
    if list(collection_generalMetroPass.find(query)):
        datafrom_generalPassMetroForm = list(collection_generalMetroPass.find(query))
    if list(collection_studentBusPass.find(query)):
        datafrom_studentPassBusForm=list(collection_studentBusPass.find(query))
    if list(collection_studentMetroPass.find(query)):
        datafrom_studentMetroBusForm=list(collection_studentMetroPass.find(query))
    data=datafrom_generalPassBusForm + datafrom_generalPassMetroForm + datafrom_studentPassBusForm + datafrom_studentMetroBusForm
    return render_template('view_transactions.html', data=data)

#function to display the active tickets

@app.route('/user_login/view_tickets/<role>/<name>/<email>')
def view_tickets(role,name,email):
    datafrom_generalPassBusForm=[]
    datafrom_generalPassMetroForm=[]
    datafrom_studentPassBusForm=[]
    datafrom_studentMetroBusForm=[]
    query = {"user_name": name, "user_email": email, "role": role,"status":"approved"}
    if list(collection_generalBusPass.find(query)):
        datafrom_generalPassBusForm = list(collection_generalBusPass.find(query))
    if list(collection_generalMetroPass.find(query)):
        datafrom_generalPassMetroForm = list(collection_generalMetroPass.find(query))
    if list(collection_studentBusPass.find(query)):
        datafrom_studentPassBusForm=list(collection_studentBusPass.find(query))
    if list(collection_studentMetroPass.find(query)):
        datafrom_studentMetroBusForm=list(collection_studentMetroPass.find(query))
    data=datafrom_generalPassBusForm + datafrom_generalPassMetroForm + datafrom_studentPassBusForm + datafrom_studentMetroBusForm
    return render_template('view_tickets.html', data=data, role=role, name=name, email=email)






#-------------------------------------------------------------------------
#------------------------------Admin Page---------------------------------
#-------------------------------------------------------------------------



def getting_data(email):
    data=[]
    datafrom_generalPassBusForm=[]
    datafrom_generalPassMetroForm=[]
    datafrom_studentPassBusForm=[]
    datafrom_studentMetroBusForm=[]
    query = {"status": "pending"}
    if list(collection_generalBusPass.find(query)):
        datafrom_generalPassBusForm = list(collection_generalBusPass.find(query))
    if list(collection_generalMetroPass.find(query)):
        datafrom_generalPassMetroForm = list(collection_generalMetroPass.find(query))
    if list(collection_studentBusPass.find(query)):
        datafrom_studentPassBusForm=list(collection_studentBusPass.find(query))
    if list(collection_studentMetroPass.find(query)):
        datafrom_studentMetroBusForm=list(collection_studentMetroPass.find(query))
    pending_data=datafrom_generalPassBusForm + datafrom_generalPassMetroForm + datafrom_studentPassBusForm + datafrom_studentMetroBusForm
    data.append(pending_data)
    datafrom_generalPassBusForm=[]
    datafrom_generalPassMetroForm=[]
    datafrom_studentPassBusForm=[]
    datafrom_studentMetroBusForm=[]
    query = {"status": "approved","admin_email":email}
    if list(collection_generalBusPass.find(query)):
        datafrom_generalPassBusForm = list(collection_generalBusPass.find(query))
    if list(collection_generalMetroPass.find(query)):
        datafrom_generalPassMetroForm = list(collection_generalMetroPass.find(query))
    if list(collection_studentBusPass.find(query)):
        datafrom_studentPassBusForm=list(collection_studentBusPass.find(query))
    if list(collection_studentMetroPass.find(query)):
        datafrom_studentMetroBusForm=list(collection_studentMetroPass.find(query))
    approved_data=datafrom_generalPassBusForm + datafrom_generalPassMetroForm + datafrom_studentPassBusForm + datafrom_studentMetroBusForm
    data.append(approved_data)
    datafrom_generalPassBusForm=[]
    datafrom_generalPassMetroForm=[]
    datafrom_studentPassBusForm=[]
    datafrom_studentMetroBusForm=[]
    query = {"status": "rejected","admin_email":email}
    if list(collection_generalBusPass.find(query)):
        datafrom_generalPassBusForm = list(collection_generalBusPass.find(query))
    if list(collection_generalMetroPass.find(query)):
        datafrom_generalPassMetroForm = list(collection_generalMetroPass.find(query))
    if list(collection_studentBusPass.find(query)):
        datafrom_studentPassBusForm=list(collection_studentBusPass.find(query))
    if list(collection_studentMetroPass.find(query)):
        datafrom_studentMetroBusForm=list(collection_studentMetroPass.find(query))
    rejected_data=datafrom_generalPassBusForm + datafrom_generalPassMetroForm + datafrom_studentPassBusForm + datafrom_studentMetroBusForm
    data.append(rejected_data)
    return data
@app.route('/admin_login')
def admin_login():
    email=session.get('email')
    data=getting_data(email)
    pending_data=data[0]
    approved_data=data[1]
    rejected_data=data[2]
    pprint.pprint(pending_data)
    return render_template('admin_login.html', message="Hi admin, welcome back!",email=session.get('email'), name=session.get('user'),role=session.get('role'),pending_data=pending_data,approved_data=approved_data,rejected_data=rejected_data)
@app.route('/admin_detail/<_id>/<email>')
def admin_detail(_id,email):
    record_type = request.args.get('record_type')
    try:
        object_id = ObjectId(_id)
    except:
        return "Invalid ID format", 400
    collections = [
        collection_generalBusPass,
        collection_generalMetroPass,
        collection_studentBusPass,
        collection_studentMetroPass
    ]
    data = None
    for collection in collections:
        result = collection.find_one({'_id': object_id})
        if result:
            data = result
            break
    if not data:
        return "Application not found", 404
    return render_template('admin_detail.html', data=data,email=email,record_type=record_type)




    app_id = request.form.get('db_id')

    try:
        object_id = ObjectId(app_id)
    except Exception as e:
        print("Invalid ObjectId:", e)
        return "Invalid ID format", 400

    collections = [
        collection_generalBusPass,
        collection_generalMetroPass,
        collection_studentBusPass,
        collection_studentMetroPass
    ]

    found_document = None
    for collection in collections:
        doc = collection.find_one({"_id": object_id})
        if doc:
            print(f"\n✅ Document found in collection: {collection.name}")
            print("📄 Document details:\n", doc)
            found_document = doc
            break

    if not found_document:
        print("❌ Document not found in any collection.")
        return "Document not found", 404

    return "Document printed in console", 200



@app.route('/update_db', methods=['POST'])
def update_db():
    app_id = request.form.get('db_id')
    admin_email = request.form.get('admin_email')

    try:
        object_id = ObjectId(app_id)
    except Exception as e:
        print("Invalid ObjectId:", e)
        return "Invalid ID format", 400

    collections = [
        collection_generalBusPass,
        collection_generalMetroPass,
        collection_studentBusPass,
        collection_studentMetroPass
    ]

    found_collection = None
    found_document = None

    # Step 1: Locate the document
    for collection in collections:
        doc = collection.find_one({"_id": object_id})
        if doc:
            print(f"✅ Document found in collection: {collection.name}")
            found_document = doc
            found_collection = collection
            break

    if not found_document:
        print("❌ Document not found in any collection.")
        return "Document not found", 404

    # Step 2: Compute Validity
    pass_type = found_document.get('pass_type', '').lower()
    start_date = datetime.now()
    
    if pass_type == 'monthly':
        end_date = start_date + timedelta(days=30)
    elif pass_type == 'quaterly':
        end_date = start_date + timedelta(days=90)
    elif pass_type == 'half-yearly':
        end_date = start_date + timedelta(days=180)
    else:
        return "Invalid pass type", 400

    validity_str = f"{start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}"
    print("🕒 Validity:", validity_str)

    # Step 3: Generate QR Code
    qr_data = {
    "name": found_document.get("name"),
    "pass_type": found_document.get("pass_type"),
    "validity": validity_str,
    "type_of_pass": found_document.get("type_of_pass"),
    "type_of_user": found_document.get("type_of_user")
    }
    qr_string = "\n".join([f"{key}: {value}" for key, value in qr_data.items()])

    qr = qrcode.make(qr_string)
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer)
    qr_buffer.seek(0)

    qr_id = fs.put(qr_buffer, filename=f"{app_id}_qr.png", content_type='image/png')
    print("✅ QR Code stored with ID:", qr_id)

    # Step 4: Update document in DB
    update_fields = {
        "status": "approved",
        "validity": validity_str,
        "qr_code": qr_id,
        "admin_email":admin_email
    }

    found_collection.update_one({"_id": object_id}, {"$set": update_fields})
    print("📌 Document updated successfully.")

    return redirect('/admin_login')

@app.route('/reject_db', methods=['POST'])
def reject_db():
    app_id = request.form.get('db_id')
    remarks = request.form.get('remarks')
    admin_email = request.form.get('admin_email')

    if not remarks:
        return "Remarks are required for rejection", 400

    try:
        object_id = ObjectId(app_id)
    except Exception as e:
        print("Invalid ObjectId:", e)
        return "Invalid ID format", 400

    collections = [
        collection_generalBusPass,
        collection_generalMetroPass,
        collection_studentBusPass,
        collection_studentMetroPass
    ]

    found_collection = None
    found_document = None

    # Step 1: Locate the document
    for collection in collections:
        doc = collection.find_one({"_id": object_id})
        if doc:
            print(f"✅ Document found in collection: {collection.name}")
            found_document = doc
            found_collection = collection
            break

    if not found_document:
        print("❌ Document not found in any collection.")
        return "Document not found", 404

    # Step 2: Update status to rejected and add remarks
    update_fields = {
        "status": "rejected",
        "remarks": remarks,
        "admin_email":admin_email
    }

    found_collection.update_one({"_id": object_id}, {"$set": update_fields})
    print("📌 Document marked as rejected with remarks.")

    return redirect('/admin_login')



def get_qr(id):
    print("----------------qr_id-----------------")
    pprint.pprint(id)
    fs = gridfs.GridFS(db)
    qr_id = ObjectId(id)  # <-- Use the actual QR ID from DB
    qr_file = fs.get(qr_id)
    qr_img = Image.open(io.BytesIO(qr_file.read()))
    qr_img.save("qr.png")
    print("QR code saved as qr.png")
@app.route('/print_id', methods=['POST'])
def print_id():
    data = request.get_json()
    print("Approved item ID:", data.get('id'))
    get_qr(data.get('id'))
    return jsonify({ 'qr_url': '/qr_code' })  # Send URL back



@app.route('/qr_code')
def serve_qr_code():
    return send_file("qr.png", mimetype='image/png') 

#function to Display the fare price table in the admin page

@app.route('/fare_prices')
def fare_prices():
    data=list(collection_fare.find())
    return render_template('fare_prices.html',data=data)

#funtion to update the fare prices in the admin page

@app.route('/update-fare', methods=['POST'])
def update_fare():
    monthly = request.form['monthly']
    quarterly = request.form['quarterly']
    half_yearly = request.form['half_yearly']
    user_type=request.form['user_type']
    print(f"Monthly: {monthly}, Quarterly: {quarterly}, Half Yearly: {half_yearly}, User Type:{user_type}")
    collection_fare.update_one(
        {"user_type": user_type},  # Match the user_type
        {"$set": {  # Update the values
            "monthly": monthly,
            "quarterly": quarterly,
            "half_yearly": half_yearly
        }}
    )
    return redirect('fare_prices')





#-------------------------------------------------------------------------
#-----------------------------Conductor Page------------------------------
#-------------------------------------------------------------------------



@app.route('/conductor_login')
def conductor_login():
    email=session.get('email')
    name=session.get('user')
    role=session.get('role')
    query={'name':name,'role':role,'email':email}
    data=list(collection_conductor.find(query))
    pprint.pprint(data)
    return render_template('conductor_login.html', message="Hi conductor, welcome back!",email=session.get('email'), name=session.get('user'),role=session.get('role'),data=data)



@app.route('/get_conductor_form_details', methods=['POST'])
def get_conductor_form_details():
    email = request.form.get('email')
    role = request.form.get('role')
    city= request.form.get('city')
    bus_no = request.form.get('bus_no')
    log_date = request.form.get('log_date')
    name=request.form.get('name')
    query={'name':name,'role':role,'email':email,'city':city,'bus_no':bus_no,'log_date':log_date}
    collection_conductor.insert_one(query)
    return redirect(url_for('conductor_login'))


#-------------------------------------------------------------------------
#---------------------------------Main------------------------------------
#-------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
