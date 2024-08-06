from flask import Flask, request, jsonify
from dbconnection import get_db_connection
import psycopg2
import json

app = Flask(__name__)
dbconn=get_db_connection()
cursor = dbconn.cursor()

@app.route("/api/signup",methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    cursor.execute("Select count(*) from public.userlogin_details")
    users_count=cursor.fetchone()[0]
    user_id = users_count + 1  
    
    insertquery=f"INSERT INTO userlogin_details (username, password, email,user_id) VALUES ('{username}','{password}','{email}',{user_id})"
    cursor.execute(insertquery)
    dbconn.commit()
    return jsonify({
        'status': 'Account successfully created',
        'status_code': 200,
        'user_id': user_id
    }), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor.execute(f"Select user_id from public.userlogin_details where username='{username}' and password='{password}'")
    login=cursor.fetchone()
    print(login)
    if(len(login)==1):
        return jsonify({
            'status': 'Login successful',
            'status_code': 200,
            'user_id': login[0],
            'access_token': "6959864tfytj565"
        }), 200
    else:
        return jsonify({
            'status': 'Incorrect username/password provided. Please retry',
            'status_code': 401
        }), 401
    
@app.route('/api/car/create', methods=['POST'])
def create_car():
    api_key = request.headers.get('API-Key')
    if not api_key=="123456balu":
        return jsonify({'status': 'Unauthorized', 'status_code': 403}), 403

    data = request.get_json()
    category = data.get('category')
    model = data.get('model')
    number_plate = data.get('number_plate')
    current_city = data.get('current_city')
    rent_per_hr = data.get('rent_per_hr')
    rent_history = data.get('rent_history')

    cursor.execute("Select count(*) from public.car_data")
    cars_count=cursor.fetchone()[0]
    car_id = cars_count + 1  

    try:
        cursor.execute(f"INSERT INTO car_data (car_id,category, model, number_plate, current_city, rent_per_hr, rent_history) VALUES ('{car_id}','{category}', '{model}', '{number_plate}', '{current_city}', {rent_per_hr}, '{json.dumps(rent_history)}')")
        
        dbconn.commit()

        return jsonify({
            'message': 'Car added successfully',
            'car_id': car_id,
            'status_code': 200
        }), 200
    except psycopg2.Error as e:
        dbconn.rollback()
        return jsonify({'status': 'Database error', 'status_code': 500, 'error': str(e)}), 500

@app.route('/api/car/get-rides', methods=['GET'])
def get_rides():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    category = request.args.get('category')
    required_hours = request.args.get('required_hours')
    print(origin)
    if not origin or not destination or not category or not required_hours:
        return jsonify({'status': 'Missing required parameters', 'status_code': 400}), 400

    try:
        required_hours = int(required_hours)
    except ValueError:
        return jsonify({'status': 'Invalid required_hours parameter', 'status_code': 400}), 400

    try:
        
        cursor.execute(f"SELECT car_id, category, model, number_plate, current_city, rent_per_hr, rent_history FROM car_data WHERE category = '{category}' AND current_city = '{origin}'")

        cars = cursor.fetchall()

        results = []
        for car in cars:
            car_id, car_category, model, number_plate, current_city, rent_per_hr, rent_history = car
            total_payable_amt = rent_per_hr * required_hours
            print(rent_history)
            rent_history_list = []
            if rent_history:
                for history in rent_history:
                    rent_history_list.append({
                        'origin': history['origin'],
                        'destination': history['destination'],
                        'amount': history['amount']
                    })

            results.append({
                'car_id': car_id,
                'category': car_category,
                'model': model,
                'number_plate': number_plate,
                'current_city': current_city,
                'rent_per_hr': rent_per_hr,
                'rent_history': rent_history_list,
                'total_payable_amt': total_payable_amt
            })

        return jsonify(results), 200
    except psycopg2.Error as e:
        return jsonify({'status': 'Database error', 'status_code': 500, 'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)