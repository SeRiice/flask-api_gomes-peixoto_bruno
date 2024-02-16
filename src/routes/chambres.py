from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Chambre, Reservation
from datetime import datetime
from sqlalchemy import and_

chambres = Blueprint("chambres", __name__)

@chambres.route("/api/chambres/disponibles", methods=["GET"])
def chambres_disponibles():
    date_arrivee = request.args.get("date_arrivee")
    date_depart = request.args.get("date_depart")

    if not(date_arrivee and date_depart):
        return jsonify({"erreur": "date_arrivee et date_depart sont requis dans les paramètres"}), 400

    if  date_arrivee > date_depart:
        return jsonify({"erreur": "date_arrivee doit être inférieure à date_depart"}), 400

    chambres_disponibles = Chambre.query.filter(
        ~Chambre.reservations.any(
           and_(
            Reservation.date_arrivee <= date_depart,
            Reservation.date_depart >= date_arrivee
            )
        )
    ).all()

    if len(chambres_disponibles) == 0:
        return jsonify({"message": "Aucune chambre disponible pour cette période."}), 200

    return [
        {
          "id": chambre.id,
          "numero": chambre.numero,
          "type": chambre.type,
          "prix": chambre.prix
        } for chambre in chambres_disponibles
      ]

@chambres.route("/api/chambres", methods=["POST"])
def creer_chambre():
    numero = request.json.get("numero")
    type = request.json.get("type")
    prix = request.json.get("prix")

    if not(numero and type and prix):
        return jsonify({"erreur": "numero, type et prix sont requis dans le corps de la requête"}), 400

    if Chambre.query.filter(Chambre.numero == numero).first():
        return jsonify({"erreur": "Chambre avec ce numéro déjà existante."}), 400

    chambre = Chambre(
        numero=numero,
        type=type,
        prix=prix
    )

    db.session.add(chambre)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Chambre créée avec succès."
    }), 201

@chambres.route("/api/chambres/<int:id>", methods=["PUT"])
def modifier_chambre(id):
    chambre = Chambre.query.get(id)

    if not chambre:
        return jsonify({"erreur": "Chambre introuvable."}), 404

    numero = request.json.get("numero")
    type = request.json.get("type")
    prix = request.json.get("prix")

    if Chambre.query.filter(Chambre.numero == numero).first():
        return jsonify({"erreur": "Numéro de chambre déjà atribué."}), 400

    if numero:
      chambre.numero = numero

    if type:
      chambre.type = type

    if prix:
      chambre.prix = prix

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Chambre mise à jour avec succès."
    })

@chambres.route("/api/chambres/<int:id>", methods=["DELETE"])
def supprimer_chambre(id):
    chambre = Chambre.query.get(id)

    if not chambre:
        return jsonify({"erreur": "Chambre introuvable."}), 404

    db.session.delete(chambre)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Chambre supprimée avec succès."
    })