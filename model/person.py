from utils.basic import Basic


class Person(Basic):
    def __init__(
            self, id, type, last_name, first_name, passport, birth_date, passport_issued, passport_expired, issued_by,
            phone: int, nationality, travel_date, start_date, end_date, family, status, script_comment, email):
        self.id = id
        self.type = type
        self.last_name = last_name
        self.first_name = first_name
        self.passport = passport
        self.birth_date = self.gdfs(birth_date)
        self.pasport_issued = self.gdfs(passport_issued)
        self.passport_expired = self.gdfs(passport_expired)
        self.issued_by = issued_by
        self.phone = phone
        self.nationality = nationality
        self.travel_date = self.gdfs(travel_date)
        self.start_date = self.gdfs(start_date)
        self.end_date = self.gdfs(end_date)
        self.family = family
        self.status = status
        self.script_comment = script_comment
        self.email = email
