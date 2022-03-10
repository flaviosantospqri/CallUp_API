from werkzeug.exceptions import BadRequest


class CnpjFormatInvalidError(BadRequest):
    ...


class EmailFormatInvalidError(BadRequest):
    ...


class PasswordFormatinvalidError(BadRequest):
    ...
