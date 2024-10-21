from backend.app import app
from flask import Flask, request, jsonify
from backend.Exceptions import *
from backend.models.plant_species_model import get_info
@app.route('/about_plant', methods=["GET"])
def get_plant_info():
    try:
        if "plant" not in request.args:
            raise MissingParamterReq("Missing plant name query parameter")

        plant = request.args.get('plant')  
        plant_info = get_info(plant)
        return jsonify(plant_info), 201
    except MissingParamterReq as e:
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

