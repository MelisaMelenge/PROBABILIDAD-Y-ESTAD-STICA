import numpy as np          # Librería para cálculos numéricos y matrices
import sympy as sp          # Librería para matemáticas simbólicas (integrales, álgebra)

print("===== CASO DISCRETO =====")

# ==========================================
# 1. MATRIZ DE PROBABILIDAD
# ==========================================
# Definimos la matriz conjunta P(X,Y)
# Filas → valores de X (bebida)
# Columnas → valores de Y (snack)
P = np.array([
    [0.10, 0.08, 0.07],   # X=0 (agua)
    [0.09, 0.16, 0.05],   # X=1 (jugo)
    [0.06, 0.14, 0.25]    # X=2 (café)
])

# ==========================================
# 2. VERIFICACIÓN
# ==========================================
# Sumamos todas las probabilidades para verificar que sea una distribución válida
suma_total = np.sum(P)
print("Suma total de probabilidades:", suma_total)

# ==========================================
# 3. PROBABILIDADES MARGINALES
# ==========================================
# Probabilidad marginal de X (sumar por filas)
PX = np.sum(P, axis=1)

# Probabilidad marginal de Y (sumar por columnas)
PY = np.sum(P, axis=0)

print("P(X):", PX)
print("P(Y):", PY)

# ==========================================
# 4. EVENTOS
# ==========================================
# a) Probabilidad conjunta específica
# Café (X=2) y sandwich (Y=2)
p_cafe_sandwich = P[2,2]
print("P(café y sandwich):", p_cafe_sandwich)

# b) Probabilidad marginal de jugo (X=1)
p_jugo = PX[1]
print("P(jugo):", p_jugo)

# c) Probabilidad de pedir algún snack (Y>=1)
p_snack = PY[1] + PY[2]
print("P(algun snack):", p_snack)

# ==========================================
# 5. PROBABILIDAD CONDICIONAL
# ==========================================
# P(Y=2 | X=2) = P(X=2,Y=2) / P(X=2)
p_condicional = P[2,2] / PX[2]
print("P(sandwich | café):", p_condicional)

# ==========================================
# 6. INDEPENDENCIA
# ==========================================
# Verificamos si P(X,Y) = P(X)*P(Y)
producto = PX[2] * PY[2]

print("P(X=2)*P(Y=2):", producto)
print("P(X=2,Y=2):", P[2,2])

# Comparación con tolerancia numérica
if abs(producto - P[2,2]) < 1e-6:
    print("Son independientes")
else:
    print("NO son independientes")



print("\n===== CASO CONTINUO =====")

# ==========================================
# VARIABLES SIMBÓLICAS
# ==========================================
# Definimos variables simbólicas para cálculo integral
x, y = sp.symbols('x y')

# Función de densidad conjunta f(x,y)
f = (1/25)*x*y

# ==========================================
# 1. VERIFICACIÓN (INTEGRAL DOBLE)
# ==========================================
# Integramos sobre todo el dominio para verificar que sea válida
integral_total = sp.integrate(
    sp.integrate(f, (y, 0, 2)),  # integral interna en y
    (x, 0, 5)                    # integral externa en x
)

print("Integral total:", integral_total)

# ==========================================
# 2. PROBABILIDAD EN REGIÓN
# ==========================================
# Calculamos P(2<=X<=4, 1<=Y<=2)
prob_region = sp.integrate(
    sp.integrate(f, (y, 1, 2)),  # límites en y
    (x, 2, 4)                    # límites en x
)

print("P(2<=X<=4, 1<=Y<=2):", prob_region)

# ==========================================
# 3. MARGINALES
# ==========================================
# f_X(x) = ∫ f(x,y) dy
fX = sp.integrate(f, (y, 0, 2))

# f_Y(y) = ∫ f(x,y) dx
fY = sp.integrate(f, (x, 0, 5))

print("f_X(x):", fX)
print("f_Y(y):", fY)

# ==========================================
# 4. CONDICIONAL
# ==========================================
# Evaluamos f_X(x) en x=4
fX_4 = fX.subs(x, 4)

# f(Y|X=4) = f(4,y) / f_X(4)
f_cond = f.subs(x, 4) / fX_4
print("f(Y|X=4):", sp.simplify(f_cond))

# Probabilidad condicional P(Y>1.5 | X=4)
prob_cond = sp.integrate(f_cond, (y, 1.5, 2))
print("P(Y>1.5 | X=4):", prob_cond)

# ==========================================
# 5. INDEPENDENCIA
# ==========================================
# Verificamos si f(x,y) = fX(x)*fY(y)
producto_cont = sp.simplify(fX * fY)

print("fX * fY:", producto_cont)
print("f(x,y):", f)

# Comparación simbólica exacta
if sp.simplify(producto_cont - f) == 0:
    print("Son independientes")
else:
    print("NO son independientes")
