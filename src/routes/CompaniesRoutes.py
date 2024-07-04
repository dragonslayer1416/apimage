from flask import Blueprint, request, jsonify
# Errors
from src.utils.errors.CustomException import CustomException
# Security
from src.utils.Security import Security
# Services
from src.services.CompaniesService import CompaniesService

main = Blueprint('companies_blueprint', __name__)


@main.route('/')
def get_companies():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            companies = CompaniesService.get_companies()
            if companies:
                return jsonify({'companies': companies, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except CustomException:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/<int:id_company>', methods=['GET'])
def get_company(id_company):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            company = CompaniesService.get_company(id_company)
            if company:
                return jsonify({'company': company, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except CustomException:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
