# =============================== #
#          BRAYTON CYCLE          #
# =============================== #

# ============ UNITS ============ #

# Mass:                   kg
# Pressure:               kPa
# Temperature:            K
# Volume:                 m ^ 3
# Work:                   kJ
# Specific volume:        (m ^ 3) / kg
# Specific heat capacity: kJ / (kg * K)
# Gas constant:           kJ / (kg * K)

# ============ INPUT ============ #

m     = float(input("m: "    ))         # Mass                                      (kg)
cp    = float(input("cp: "   ))         # Specific heat at constant pressure        (kJ / (kg * K))
gamma = float(input("gamma: "))         # heat capacity ratio                       (dimensionless)
T1    = float(input("T1: "   ))         # Compressor inlet temperature              (K)
P1    = float(input("P1: "   ))         # Compressor inlet pressure                 (kPa)
rp    = float(input("rp: "   ))         # Pressure ratio                            (dimensionless)
T3    = float(input("T3: "   ))         # Maximum cycle temperature                 (K)

# ======= STATE VARIABLES ======= #

P2 = P1 * rp                            # Compressor outlet pressure                (kPa)
P3 = P2                                 # Turbine inlet pressure                    (kPa)
P4 = P1                                 # Turbine outlet pressure                   (kPa)

T2 = T1 * (rp ** ((gamma - 1) / gamma)) # Compressor outlet temperature             (K)
T4 = T3 / (rp ** ((gamma - 1) / gamma)) # Turbine outlet temperature                (K)

R = ((gamma - 1) * cp) / gamma          # Gas constant                              (kJ / (kg * K))
v1 = R * T1 / P1                        # Compressor inlet specific volume          ((m ^ 3) / kg)
v2 = R * T2 / P2                        # Compressor outlet specific volume         ((m ^ 3) / kg)
v3 = R * T3 / P3                        # Turbine inlet specific volume             ((m ^ 3) / kg)
v4 = R * T4 / P4                        # Turbine outlet specific volume            ((m ^ 3) / kg)

# ============ WORK ============= #

Wc   = m * cp * (T2 - T1)               # Compressor work                           (kJ)
Wt   = m * cp * (T3 - T4)               # Turbine work                              (kJ)
Wnet = Wt - Wc                          # Net work                                  (kJ)

# ============ HEAT ============= #

Qin  = m * cp * (T3 - T2)               # Heat added                                (kJ)
Qout = m * cp * (T4 - T1)               # Heat rejected                             (kJ)

# ========= EFFICIENCY ========== #

eta  = Wnet / Qin                       # Thermal efficiency                        (dimensionless)
bwr  = Wc / Wt                          # Back Work Ratio                           (dimensionless)

# ============ DEBUG ============ #
# debug (remove later):

print(f"(P1, V1) = ({P1}, {v1})"    )
print(f"(P2, V2) = ({P2}, {v2})"    )
print(f"(P3, V3) = ({P3}, {v3})"    )
print(f"(P4, V4) = ({P4}, {v4})"    )
print(""                            )
print(f"Compressor work = {Wc} kJ"  )
print(f"Turbine work    = {Wt} kJ"  )
print(f"Net work        = {Wnet} kJ")
print(""                            )
print(f"Heat added = {Qin} kJ"      )
print(f"Heat rejected = {Qout} kJ"  )
print(""                            )
print(f"Efficiency = {eta}"         )
print(f"Back work ratio = {bwr}"    )

# =============================== #