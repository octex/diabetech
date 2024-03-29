from http.client import NOT_ACCEPTABLE


class HTTPMethods:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"

class HTTPCodes:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    INTERNAL_ERROR = 500

class Config:
    DB_PATH = ""
    MAX_PAGINATION_SET = 10
