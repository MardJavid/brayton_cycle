# =============================== #
#            FUNCTIONS            #
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

# =============================== #


# Returns an array containing 4 tuples of (P, v, T) in (kPa, (m ^ 3) / kg)
# Input:
# P1    - Compressor inlet pressure          (kPa)
# T1    - Compressor inlet temperature       (K)
# T3    - Maximum cycle temperature          (K)
# rp    - Pressure ratio                     (dimensionless)
# cp    - Specific heat at constant pressure (kJ / (kg * K))
# gamma - heat capacity ratio                (dimensionless)
def getStateVariables(P1, T1, T3, rp, cp, gamma):
    if P1 <= 0:
        raise ValueError("Pressure must be more than 0.")

    if T1 <= 0 or T3 <= 0:
        raise ValueError("Temperature must be more than 0.")

    if rp <= 0:
        raise ValueError("Pressure ratio must be more than 0.")

    if cp <= 0:
        raise ValueError("Specific heat must be more than 0.")

    if gamma <= 1:
        raise ValueError("Gamma must be more than 1.")

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

    return [
        (P1, v1, T1),
        (P2, v2, T2),
        (P3, v3, T3),
        (P4, v4, T4),
    ]

# Returns a tuple containing Compressor work, turbine work and net work in order
# Input:
# m  - Mass                               (kg)
# cp - Specific heat at constant pressure (kJ / (kg * K))
# T1 - Compressor inlet temperature       (K)
# T2 - Compressor outlet temperature      (K)
# T3 - Maximum cycle temperature          (K)
# T4 - Turbine outlet temperature         (K)
def getWork(m, cp, T1, T2, T3, T4):    
    if (m <= 0):
        raise ValueError("Mass must be more than 0.")

    if cp <= 0:
        raise ValueError("Specific heat must be more than 0.")
    
    if T1 <= 0 or T2 <= 0 or T3 <= 0 or T4 <= 0:
        raise ValueError("Temperature must be more than 0.")

    if T2 <= T1:
        raise ValueError("T2 must be greater than T1")

    if T3 <= T4:
        raise ValueError("T3 must be greater than T4")
    
    Wc   = m * cp * (T2 - T1)               # Compressor work                           (kJ)
    Wt   = m * cp * (T3 - T4)               # Turbine work                              (kJ)
    Wnet = Wt - Wc                          # Net work                                  (kJ)
    return (Wc, Wt, Wnet)

# Returns a tuple containing heat added, heat rejected, thermal efficiency and back work ratio in order
# Input:
# m    - Mass                               (kg)
# cp   - Specific heat at constant pressure (kJ / (kg * K))
# T1   - Compressor inlet temperature       (K)
# T2   - Compressor outlet temperature      (K)
# T3   - Maximum cycle temperature          (K)
# T4   - Turbine outlet temperature         (K)
# Wc   - Compressor work                    (kJ)
# Wt   - Turbine work                       (kJ)
# Wnet - Net work                           (kJ)
def getHeat(m, cp, T1, T2, T3, T4, Wc, Wt, Wnet):
    if m <= 0:
        raise ValueError("Mass must be more than zero.")

    if cp <= 0:
        raise ValueError("Specific heat must be more than 0.")

    if T1 <= 0 or T2 <= 0 or T3 <= 0 or T4 <= 0:
        raise ValueError("Temperature must be more than 0.")    

    if T2 <= T1:
        raise ValueError("T2 must be greater than T1")

    if T3 <= T4:
        raise ValueError("T3 must be greater than T4")

    if Wt <= Wc or Wnet <= 0:
        raise ValueError("Net work must be positive")

    Qin  = m * cp * (T3 - T2)               # Heat added                                (kJ)
    Qout = m * cp * (T4 - T1)               # Heat rejected                             (kJ)
    eta  = Wnet / Qin                       # Thermal efficiency                        (dimensionless)
    bwr  = Wc / Wt                          # Back Work Ratio                           (dimensionless)
    return (Qin, Qout, eta, bwr)