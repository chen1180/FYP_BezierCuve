import math

Ts=130
Tair=24
D=0.25
v=2.097e-5
Pr=0.7154
k=0.02953

g=9.81
sigma=5.67e-8


def cylinder_natural_convection(Ts,Tair,D,v,Pr,k,emissity,A):
    Tf = (Ts + Tair) / 2.0  # in degree celcius
    beta = 1 / (Tf + 273)
    Rad = (g * beta * (Ts - Tair) * math.pow(D, 3) / math.pow(v, 2)) * Pr
    Nud = math.pow(0.6 + 0.387 * math.pow(Rad, 1 / 6) / math.pow(1 + math.pow(0.559 / Pr, 9 / 16), 8 / 27), 2)
    h_bar = Nud * k / D

    Qconv = h_bar * A * (Ts - Tair)
    Qrad = A * sigma * emissity * (math.pow(Ts + 273, 4) - math.pow(Tair + 273, 4))
    Qt=Qconv+Qrad
    print(Qt)
def plate_natural_convection(Ts,Tair,D,v,Pr,k,emissity,A):
    Tf = (Ts + Tair) / 2.0  # in degree celcius
    beta = 1 / (Tf + 273)
    L=A/(4*D)
    Ral = (g * beta * (Ts - Tair) * math.pow(L, 3) / math.pow(v, 2)) * Pr
    Nud = 0.68 + 0.67*math.pow(Ral,1/4)/math.pow(1+math.pow(0.492/Pr,9/16),4/9)
    # Nud=0.81*math.pow(Ral,1/4)
    h_bar = Nud * k / L
    print(L,Ral,Nud,h_bar)
    Qconv = h_bar * A * (Ts - Tair)
    Qrad = A * sigma * emissity * (math.pow(Ts + 273, 4) - math.pow(Tair + 273, 4))
    Qt=Qconv+Qrad
    print(Qt)
#Q1
# plate_natural_convection(Ts=130,
#                          Tair=24,
#                          D=0.25,
#                          v=2.097e-5,
#                          Pr=0.7154,
#                          k=0.02953,emissity=0.9,A = math.pi * math.pow(D, 2) / 4)
# #Q2
# cylinder_natural_convection(Ts=150,
#                          Tair=25,
#                          D=70e-3,
#                          v=2.201e-5,
#                          Pr=0.7132,
#                          k=0.03024,emissity=0.8,A=math.pi *D)
#Q3
k=1.4
Cp=835
rho=2225
alpha=k/rho/Cp
Pr=v/alpha
cylinder_natural_convection(Ts=90,
                         Tair=25,
                         D=200e-3,
                         v=2.097e-5,
                         Pr=0.7154,
                         k=0.02953,emissity=0.8,A = math.pow(200e-3,2))
print(math.pow(0.6 + 0.387 * math.pow(0.19145, 1 / 6) / math.pow(1 + math.pow(0.559 / 4.56, 9 / 16), 8 / 27), 2))