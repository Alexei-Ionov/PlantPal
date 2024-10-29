from backend.app import app
from flask import Flask, request, jsonify, redirect, url_for, session
from backend.models.user_model import *
from backend.Exceptions import *
from backend.models.sensor_updates import check_token_and_process_update

@app.route('/add_esp', methods=["POST"])
def add_esp():
    try: 
        user_id = session["user_id"]
        esp_info = request.json
        if "esp32_ip" not in esp_info:
            raise Exception InvalidInputError("Missing esp ip")
        if "token" not in esp_info:
            raise Exception InvalidInputError("Missing token")
        esp32_ip = esp_info["esp32_ip"]
        token = esp_info["token"]
        add_esp_to_user_plant(user_id, token, esp32_ip)
        
        return jsonify({
            "message": "successfully updated esp ip for user plant"
        }), 201


    except InvalidInputError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

@app.route('/update_sensor_reading', methods = ["POST"])
def update_sensor_reading():
    try: 
        sensor_data = request.json
        if "soil_moisture" not in sensor_data:
            raise InvalidSensorReq("ESP32 failed to send soil_moisture in request")
        if "token" not in sensor_data:
            raise InvalidSensorReq("ESP32 failed to send token in request")

        current_soil_moisture = sensor_data["soil_moisture"]
        token = sensor_data["token"]

        check_token_and_process_update(current_soil_moisture, token)
        return jsonify({
            "msg": "successfully updated sensor reading!"
        }), 201

    #NOTE -> might not even return anything since communication with esp32 is really just one way esp32 -> server
    except InvalidSensorReq as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

