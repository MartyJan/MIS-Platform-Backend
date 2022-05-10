""" Exchanges Namespace's API """

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from models import Exchange
from datetime import datetime

exchange_api=Namespace('exchanges')

exchange_model = exchange_api.model(
    "exchanges",
    {
        "id": fields.Integer(),
        "receiver_uid": fields.Integer(),
        "provider_uid": fields.Integer(),
        "item": fields.String(),
        "region": fields.String(),
        "status": fields.String(),
        "notes": fields.String(),
        "date_added": fields.DateTime(default=datetime.now)
    }
)


@exchange_api.route("/")
class ExchangesResource(Resource):
    
    @exchange_api.marshal_list_with(exchange_model)
    def get(self):
        """ Get all exchanges """
        exchanges = Exchange.query.all()
        return exchanges
    
    @exchange_api.marshal_with(exchange_model)
    @exchange_api.expect(exchange_model)
    @jwt_required()
    def post(self):
        """ Create a new exchange """
        """ 
            @jwt_required() means JWT authenitcation is needed
            Request header needs to include the following:
                "Authorization": "Bearer <access_token>"
        """
        data = request.get_json()

        new_exchange = Exchange(
            receiver_uid = data.get("receiver_uid"),
            provider_uid = data.get("provider_uid"),
            item = data.get("item"),
            region = data.get("region"),
            status = data.get("status"),
            notes =  data.get("notes"),
        )
        
        new_exchange.save()
        return new_exchange
    
        
@exchange_api.route("/<int:id>")
class ExchangeResource(Resource):
    @exchange_api.marshal_with(exchange_model)
    def get(self, id):
        """ Get an exchange by id """
        exchange = Exchange.query.get_or_404(id)
        return exchange
    
    @exchange_api.marshal_with(exchange_model)
    @jwt_required()
    def put(self, id):
        """ Update an exchange by id """
        exchange_to_update = Exchange.query.get_or_404(id)
        data = request.get_json()
        if "status" in data:
            exchange_to_update.update_status(data.get("status"))
        if "provider_uid" in data:
            exchange_to_update.update_provider(data.get("provider_uid"))
        return exchange_to_update
    
    @exchange_api.marshal_with(exchange_model)
    @jwt_required()
    def delete(self, id):
        """ Delete an exchange """
        exchange_to_delete = Exchange.query.get_or_404(id)
        exchange_to_delete.delete()
        return exchange_to_delete
    

@exchange_api.route("/<int:uid>/demand")
class UserDemand(Resource):
    
    @exchange_api.marshal_with(exchange_model)
    def get(self, uid):
        """ Get a user's demand by his uid """
        demand = Exchange.query.filter(Exchange.receiver_uid==uid).all()
        return demand


@exchange_api.route("/<int:uid>/supply")
class UserSupply(Resource):
    
    @exchange_api.marshal_with(exchange_model)
    def get(self, uid):
        """ Get a user's supply by his uid """
        supply = Exchange.query.filter(Exchange.provider_uid==uid).all()
        return supply