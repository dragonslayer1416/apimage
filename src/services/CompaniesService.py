# src/services/CompaniesService.py

from src.database.db import get_connection
from src.utils.errors.CustomException import CustomException
from .models.Company import Company

class CompaniesService:

    @classmethod
    def get_companies(cls):
        try:
            connection = get_connection()
            companies = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_company, name_company, dba_company, fein_company, address_company, apartment_company, cityzip_company, county_company, mailing_address, cityzip_mailing, phonenumber_company, id_taxation, id_business, id_state, id_status, id_user, id_location FROM companies')
                resultset = cursor.fetchall()
                for row in resultset:
                    company = Company(
                        id_company=int(row[0]),
                        name_company=row[1],
                        dba_company=row[2],
                        fein_company=row[3],
                        address_company=row[4],
                        apartment_company=row[5],
                        cityzip_company=row[6],
                        county_company=row[7],
                        mailing_address=row[8],
                        cityzip_mailing=row[9],
                        phonenumber_company=row[10],
                        id_taxation=row[11],
                        id_business=row[12],
                        id_state=row[13],
                        id_status=row[14],
                        id_user=row[15],
                        id_location=row[16]
                    )
                    companies.append(company.to_json())
            connection.close()
            return companies
        except Exception as ex:
            raise CustomException(ex)

    @classmethod
    def get_company(cls, id_company):
        try:
            connection = get_connection()
            company = None
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_company, name_company, dba_company, fein_company, address_company, apartment_company, cityzip_company, county_company, mailing_address, cityzip_mailing, phonenumber_company, id_taxation, id_business, id_state, id_status, id_user, id_location FROM companies WHERE id_company = %s', (id_company,))
                row = cursor.fetchone()
                if row:
                    company = Company(
                        id_company=int(row[0]),
                        name_company=row[1],
                        dba_company=row[2],
                        fein_company=row[3],
                        address_company=row[4],
                        apartment_company=row[5],
                        cityzip_company=row[6],
                        county_company=row[7],
                        mailing_address=row[8],
                        cityzip_mailing=row[9],
                        phonenumber_company=row[10],
                        id_taxation=row[11],
                        id_business=row[12],
                        id_state=row[13],
                        id_status=row[14],
                        id_user=row[15],
                        id_location=row[16]
                    )
            connection.close()
            return company.to_json() if company else None
        except Exception as ex:
            raise CustomException(ex)
