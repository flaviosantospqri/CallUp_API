import re

from app.exc.provider_exc import CnpjFormatInvalidError, EmailFormatInvalidError, PasswordFormatinvalidError

def validate_email(email):

    patter = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}\.?[a-zA-Z\.a-zA-Z]{1,3}?$")
    
    if not re.fullmatch(patter, email):
        raise EmailFormatInvalidError


def validate_cnpj(cnpj):

    patter = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})")
    
    if not re.fullmatch(patter, cnpj):
        raise CnpjFormatInvalidError


    for signal in [".", "-", "/"]:
        cnpj = cnpj.replace(signal, "")

    return cnpj


def validate_password(password):

    patter = re.compile(r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$")

    if not re.fullmatch(patter, password):
        raise PasswordFormatinvalidError