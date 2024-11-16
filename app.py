from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  
    'database': 'weather_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if city and start_date and end_date:
        query = """
        SELECT * FROM Weather 
        WHERE city = %s AND date BETWEEN %s AND %s
        """
        cursor.execute(query, (city, start_date, end_date))
    elif city:
        query = "SELECT * FROM Weather WHERE city = %s"
        cursor.execute(query, (city,))
    else:
        cursor.execute("SELECT * FROM Weather")
    
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/weather', methods=['POST'])
def add_weather():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Weather (city, date, temperature, humidity, description)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data['city'], data['date'], data['temperature'], data['humidity'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Weather data added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
