from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Reservation, Client, Chambre

reservations = Blueprint("reservations", __name__)

@reservations.route("/api/reservations", methods=["POST"])
def creer_reservation():
  id_client = request.json.get("id_client")
  id_chambre = request.json.get("id_chambre")
  date_arrivee = request.json.get("date_arrivee")
  date_depart = request.json.get("date_depart")

  if not(id_client and id_chambre and date_arrivee and date_depart):
    return jsonify({"erreur": "id_client, id_chambre, date_arrivee et date_depart sont requis dans le corps de la requête"}), 400
  
  if date_arrivee > date_depart:
    return jsonify({"erreur": "date_arrivee doit être inférieure à date_depart"}), 400
  
  if Reservation.query.filter(
    Reservation.id_chambre == id_chambre,
    Reservation.date_arrivee <= date_depart,
    Reservation.date_depart >= date_arrivee
  ).first():
    return jsonify({"erreur": "Chambre déjà réservée pour cette période."}), 400

  if not Client.query.get(id_client):
    return jsonify({"erreur": "Client inexistant."}), 400
  
  if not Chambre.query.get(id_chambre):
    return jsonify({"erreur": "Chambre inexistante."}), 400

  reservation = Reservation(
    id_client=id_client,
    id_chambre=id_chambre,
    date_arrivee=date_arrivee,
    date_depart=date_depart,
    statut="En attente"
  )

  db.session.add(reservation)
  db.session.commit()

  return jsonify({
    "success": True,
    "message": "Réservation créée avec succès."
  }), 201

@reservations.route("/api/reservations/<int:id>", methods=["DELETE"])
def annuler_reservation(id):
  reservation = Reservation.query.get(id)

  if not reservation:
    return jsonify({"erreur": "Réservation inexistante."}), 400
  
  db.session.delete(reservation)
  db.session.commit()

  return jsonify({
    "success": True,
    "message": "Réservation annulée avec succès."
  })