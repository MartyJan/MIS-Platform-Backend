""" Accounts Namespace's API """

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response
from models import Account
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

account_api=Namespace('accounts')

account_model = account_api.model(
    "accounts",
    {
        "uid": fields.Integer(),
        "line_id": fields.String(),
        "line_user_id": fields.String(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    }
)


@account_api.route("/signup")
class SignUp(Resource):
    # @account_api.marshal_list_with(account_model)
    @account_api.expect(account_model)
    def post(self):
        """ Create a new account """
        data = request.get_json()
        
        # Use email as an identifier
        signup_email = data.get("email")
        db_account = Account.query.filter(Account.email==signup_email).first()
        
        if db_account is not None:
            return jsonify({"message": f"User with email {signup_email} already exists."})
        
        """ TODO: get line_user_id """
        signup_line_user_id = '12345'
        
        new_account = Account(
            line_id = data.get("line_id"),
            line_user_id = signup_line_user_id,
            username =  data.get("username"),
            email = data.get("email"),
            password =  generate_password_hash(data.get("password"))
        )
        
        new_account.save()
        # return new_account
        return make_response(jsonify({"message":"Account created successfuly"}),201)


@account_api.route("/login")
class Login(Resource):  
    @account_api.expect(account_model)
    def post(self):
        """ Login an account """
        data = request.get_json()
        login_email = data.get("email")
        login_password = data.get("password")
        
        db_account = Account.query.filter(Account.email == login_email).first()
        
        if db_account is not None and check_password_hash(db_account.password, login_password):
            access_token = create_access_token(identity=db_account.email)
            refresh_token = create_refresh_token(identity=db_account.email)
            
            return jsonify(
                {
                    "uid": db_account.uid,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )
        elif db_account is not None:
            return jsonify({"message": "Wrong password."})
        else:
            return jsonify({"message": "Account not found."})


@account_api.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({"access_token":new_access_token}),200)
