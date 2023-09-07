def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remover caracteres não numéricos

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    # Calcular o primeiro dígito verificador
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    if remainder < 2:
        digito1 = 0
    else:
        digito1 = 11 - remainder

    if int(cpf[9]) != digito1:
        return False

    # Calcular o segundo dígito verificador
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    if remainder < 2:
        digito2 = 0
    else:
        digito2 = 11 - remainder

    if int(cpf[10]) != digito2:
        return False

    return True
