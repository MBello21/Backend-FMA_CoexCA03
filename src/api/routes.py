from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from flask_cors import CORS
from sqlalchemy import select, func
from api.models import db, Meteorological, Recommendation

api = Blueprint('api', __name__)

CORS(api)


@api.route('/temperature', methods=['GET'])
def get_temperature():
    result = Meteorological.query.filter_by(freak='temperatura').all()
    return jsonify([f.serialize() for f in result]), 200


@api.route('/temperature', methods=['POST'])
def post_temperature():
    data = request.get_json()
    
    required_fields=["freak", "cat", "title"]
    missing = [req for req in required_fields if not data.get(req)]
    
    if missing:
        return jsonify({'error': 'All fields are required'}), 400

    recommendations = data.get("recommendation_list")
    new_meteorological = Meteorological(
        freak=data.get("freak", "temperatura"),
        cat=data.get("cat"),
        title=data.get("title"),
    )
    
    db.session.add(new_meteorological)
    db.session.commit()
    
    for recommendation in recommendations:
        new_recommendation = Recommendation(
            freak_id= new_meteorological.id,
            recommendation= recommendation
        )
        db.session.add(new_recommendation)
        db.session.commit()

    return jsonify({
        "msg": "Created successfully",
        "recommendation": new_meteorological.serialize()
    }), 201

@api.route("/temperature-recommendation/<id>",methods=["PATCH"])
def patch_recommendation(id):
    data = request.get_json()
    
    required_fields = ["new_recommendation"]
    missing = [req for req in required_fields if not data.get(req)]
    
    if missing:
        return jsonify({'error': 'All fields are required'}), 400
    
    recommendation = db.session.execute(select(Recommendation).where(Recommendation.id == id)).scalar_one_or_none()
    if not recommendation:
        return jsonify({"error": "Recommendation not found"}), 400
    recommendation.recommendation = data.get("new_recommendation")
    db.session.commit()
    
    return jsonify({"msg":"ok"}),200
    