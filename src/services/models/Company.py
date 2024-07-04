class Company():

    def __init__(self, id_company, name_company, dba_company, fein_company, address_company, apartment_company, cityzip_company, county_company, mailing_address, cityzip_mailing, phonenumber_company, id_taxation, id_business, id_state, id_status, id_user, id_location ) -> None:
        self.id_company = id_company
        self.name_company = name_company
        self.dba_company = dba_company
        self.fein_company = fein_company
        self.address_company = address_company
        self.apartment_company = apartment_company
        self.cityzip_company = cityzip_company
        self.county_company = county_company
        self.mailing_address = mailing_address
        self.cityzip_mailing = cityzip_mailing
        self.phonenumber_company = phonenumber_company
        self.id_taxation = id_taxation
        self.id_business = id_business
        self.id_state = id_state
        self.id_status = id_status
        self.id_user = id_user
        self.id_location = id_location

    def to_json(self):
        return {
            'id_company': self.id_company,
            'name_company': self.name_company,
            'dba_company': self.dba_company,
            'fein_company': self.fein_company,
            'address_company': self.address_company,
            'apartment_company': self.apartment_company,
            'cityzip_company': self.cityzip_company,
            'county_company': self.county_company,
            'mailing_address': self.mailing_address,
            'cityzip_mailing': self.cityzip_mailing,
            'phonenumber_company': self.phonenumber_company,
            'id_taxation': self.id_taxation,
            'id_business': self.id_business,
            'id_state': self.id_state,
            'id_status': self.id_status,
            'id_user': self.id_user,
            'id_location': self.id_location
        }
