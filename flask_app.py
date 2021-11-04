import json
from flask import Flask, request, jsonify, render_template, url_for, redirect

from filtering import filter, preprocessUserData
from csv_manager import add_new_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api", methods=['POST'])
def calculate_sim():
    if request.method == 'POST':
        #get user data from post
        request_data = request.get_json()
        
        user_data = [
            request_data['userId'],
            request_data["interest"],
            request_data['occupation'],
            request_data['birthdate'],
            request_data['follow_count'],
            request_data['latitude'],
            request_data['longitude'],
        ]
        
        #preprocess user data
        processed_user_data = preprocessUserData(user_data)
        #calculate similarities and getting the names
        recommended_ids = filter(processed_user_data)
        #add the new data to current csv file
        add_new_data('data/data.csv', user_data)
        
        #sending back to app
        result = json.dumps(recommended_ids)
    
        return jsonify(result)

if __name__ == "__main__":        
    app.run()                     