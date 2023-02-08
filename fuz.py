def triangular_mf(x, a, b, c):
    if x <= a:
        return 0
    elif x > a and x < b:
        return (x - a) / (b - a)
    elif x >= b and x < c:
        return (c - x) / (c - b)
    else:
        return 0

def fuzzy_logic_mamdani(position, error_position):

    # Membership function for position
    position_low = triangular_mf(position, -20, -15, 0)
    position_medium = triangular_mf(position, -15, 0, 15)
    position_high = triangular_mf(position, 0, 15, 20)

    # Membership function for error_position
    error_position_negatif = triangular_mf(error_position, -20, -15, 0)
    error_position_nol = triangular_mf(error_position, -15, 0, 15)
    error_position_positif = triangular_mf(error_position, 0, 15, 20)

    # Rule base
    rule_base = [
        (min(position_low, error_position_negatif), 'fast'),
        (min(position_low, error_position_nol), 'normal'),
        (min(position_low, error_position_positif), 'slow'),
        (min(position_medium, error_position_negatif), 'fast'),
        (min(position_medium, error_position_nol), 'normal'),
        (min(position_medium, error_position_positif), 'normal'),
        (min(position_high, error_position_negatif), 'normal'),
        (min(position_high, error_position_nol), 'slow'),
        (min(position_high, error_position_positif), 'slow')
    ]

    # Defuzzification
    defuzzified_value = 0
    total_weight = 0
    for r in rule_base:
        weight = r[0]
        if weight > 0:
            if r[1] == 'slow':
                defuzzified_value += weight * -100
                total_weight += weight
            elif r[1] == 'normal':
                defuzzified_value += weight * 0
                total_weight += weight
            elif r[1] == 'fast':
                defuzzified_value += weight * 100
                total_weight += weight

    speed = defuzzified_value / total_weight
    return int(speed)

target = 0
posisi = 10
error =  10
speed = fuzzy_logic_mamdani(posisi,error)
print("speed Motor:", speed)