# Fungsi fuzzyfikasi triangular
def triangular_mf(x, a, b, c):
    if x <= a:
        return 0
    elif x > a and x < b:
        return (x - a) / (b - a)
    elif x >= b and x < c:
        return (c - x) / (c - b)
    else:
        return 0

# Variabel input
suhu = 25
delta = 0

# Fungsi keanggotaan variabel input suhu
dingin = triangular_mf(suhu, 18, 18, 23)
sejuk = triangular_mf(suhu, 18, 23, 28)
panas = triangular_mf(suhu, 23, 28, 28)

# Fungsi keanggotaan variabel input delta sensor suhu
negatif = triangular_mf(delta, -5, -5, 0)
nol = triangular_mf(delta, -5, 0, 5)
positif = triangular_mf(delta, 0, 5, 5)

# Variabel output
lambat = {0: 0, 1: 0, 2: 30}
sedang = {0: 20, 1: 30, 2: 40}
cepat = {0: 35, 1: 50, 2: 50}

# Rule base
rules = {
    (dingin, negatif): lambat,
    (dingin, nol): lambat,
    (dingin, positif): sedang,
    (sejuk, negatif): lambat,
    (sejuk, nol): sedang,
    (sejuk, positif): cepat,
    (panas, negatif): sedang,
    (panas, nol): cepat,
    (panas, positif): cepat,
}

# Inferensi
rule_values = []
for rule in rules:
    rule_value = min([rule[0], rule[1]]) * min([rules[rule][x] for x in rules[rule]])
    rule_values.append((rule, rule_value))

# Defuzzifikasi
numerator = 0.0
denominator = 0.0
for output in [lambat, sedang, cepat]:
    output_values = []
    for rule, rule_value in rule_values:
        if rules[rule] == output:
            output_values.append(rule_value)
    if len(output_values) > 0:
        output_value = max(output_values)
        output_center = sum([float(x) * output[x] for x in output]) / sum(output.values())
        numerator += output_value * output_center
        denominator += output_value
if denominator != 0.0:
    kecepatan = numerator / denominator

# Hasil
print("Kecepatan: ", kecepatan)