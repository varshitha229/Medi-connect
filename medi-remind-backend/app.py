# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# app = Flask(__name__)
# CORS(app)  # Allow requests from frontend

# # MongoDB Atlas Connection
# MONGO_URI = "mongodb+srv://varshi141178:GKgGrwJPnXz8hexs@cluster0.wfx01.mongodb.net/"
# client = MongoClient(MONGO_URI)
# db = client["medi_connect"]  # Database Name
# patients_collection = db["patients"]   # Patients Collection
# reminders_collection = db["reminders"]  # Medication Reminders Collection

# # ✅ **1. Get All Patients (Supports Search)**
# @app.route("/api/patients", methods=["GET"])
# def get_patients():
#     search_term = request.args.get("search", "").strip()
#     query = {"name": {"$regex": search_term, "$options": "i"}} if search_term else {}
#     patients = list(patients_collection.find(query, {"_id": 0}))  # Exclude ObjectId
#     return jsonify(patients)

# # ✅ **2. Add New Patient**
# @app.route("/api/patients", methods=["POST"])
# def add_patient():
#     data = request.json
#     patients_collection.insert_one(data)
#     return jsonify({"message": "Patient added successfully!"}), 201

# # ✅ **3. Edit Patient Details**
# @app.route("/api/patients/<id>", methods=["PUT"])
# def edit_patient(id):
#     data = request.json
#     patients_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#     return jsonify({"message": "Patient updated successfully!"})

# # ✅ **4. Delete Patient**
# @app.route("/api/patients/<id>", methods=["DELETE"])
# def delete_patient(id):
#     patients_collection.delete_one({"_id": ObjectId(id)})
#     return jsonify({"message": "Patient deleted successfully!"})

# # ✅ **5. Get All Medication Reminders**
# @app.route("/api/reminders", methods=["GET"])
# def get_reminders():
#     reminders = list(reminders_collection.find({}, {"_id": 0}))  # Exclude ObjectId
#     return jsonify(reminders)

# # ✅ **6. Add Medication Reminder**
# @app.route("/api/reminders", methods=["POST"])
# def add_reminder():
#     new_reminder = request.json
#     reminders_collection.insert_one(new_reminder)
#     return jsonify({"message": "Reminder added successfully!"}), 201

# # ✅ **7. Delete Medication Reminder**
# @app.route("/api/reminders/<id>", methods=["DELETE"])
# def delete_reminder(id):
#     reminders_collection.delete_one({"_id": ObjectId(id)})
#     return jsonify({"message": "Reminder deleted successfully!"})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow requests from frontend

# 🔹 MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://varshi141178:GKgGrwJPnXz8hexs@cluster0.wfx01.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["medi_connect"] 
print("Collections:", db.list_collection_names())# Database Name
patients_collection = db["patients"]   # Patients Collection
reminders_collection = db["reminders"]  # Medication Reminders Collection

# # ✅ **1. Get All Patients (Supports Search)**
# @app.route("/api/patients", methods=["GET"])
# def get_patients():
#     search_term = request.args.get("search", "").strip()
#     query = {"name": {"$regex": search_term, "$options": "i"}} if search_term else {}
    
#     patients = list(patients_collection.find(query))
#     for patient in patients:
#         patient["_id"] = str(patient["_id"])  # Convert ObjectId to string
    
#     return jsonify(patients)
@app.route("/api/patients", methods=["GET"])
def get_patients():
    try:
        search_term = request.args.get("search", "")
        search_term = search_term.strip() if search_term else ""

        query = {"name": {"$regex": search_term, "$options": "i"}} if search_term else {}

        patients = list(patients_collection.find(query))
        for patient in patients:
            patient["_id"] = str(patient["_id"])  # Convert ObjectId to string

        return jsonify(patients), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# ✅ **2. Add New Patient (Validation Included)**
@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.json

    # 🔹 Validate required fields
    if not data.get("name") or not data.get("age") or not data.get("medical_history"):
        return jsonify({"error": "Missing required fields (name, age, medical_history)"}), 400

    new_patient = {
        "name": data["name"],
        "age": data["age"],
        "medical_history": data["medical_history"]
    }
    
    result = patients_collection.insert_one(new_patient)
    new_patient["_id"] = str(result.inserted_id)

    return jsonify({"message": "Patient added successfully!", "patient": new_patient}), 201

# ✅ **3. Edit Patient Details**
@app.route("/api/patients/<id>", methods=["PUT"])
def edit_patient(id):
    data = request.json

    # 🔹 Validate that the patient exists
    if not patients_collection.find_one({"_id": ObjectId(id)}):
        return jsonify({"error": "Patient not found"}), 404

    patients_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    return jsonify({"message": "Patient updated successfully!"})

# ✅ **4. Delete Patient**
@app.route("/api/patients/<id>", methods=["DELETE"])
def delete_patient(id):
    result = patients_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"message": "Patient deleted successfully!"})

# ✅ **5. Get All Medication Reminders**
@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    reminders = list(reminders_collection.find())

    for reminder in reminders:
        reminder["_id"] = str(reminder["_id"])  # Convert ObjectId to string
    
    return jsonify(reminders)

# ✅ **6. Add Medication Reminder (Validation Included)**
@app.route("/api/reminders", methods=["POST"])
def add_reminder():
    data = request.json

    # 🔹 Validate required fields
    if not data.get("reminder") or not data.get("time"):
        return jsonify({"error": "Missing required fields (reminder, time)"}), 400

    new_reminder = {
        "reminder": data["reminder"],
        "time": data["time"]
    }

    result = reminders_collection.insert_one(new_reminder)
    new_reminder["_id"] = str(result.inserted_id)

    return jsonify({"message": "Reminder added successfully!", "reminder": new_reminder}), 201

# ✅ **7. Delete Medication Reminder**
@app.route("/api/reminders/<id>", methods=["DELETE"])
def delete_reminder(id):
    result = reminders_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Reminder not found"}), 404

    return jsonify({"message": "Reminder deleted successfully!"})

# ✅ **Run Flask Server**
# ✅ Start Flask App on Render’s Dynamic Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
