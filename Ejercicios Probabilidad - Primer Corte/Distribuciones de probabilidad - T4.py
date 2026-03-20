# ==========================================
# LIBRERIAS
# ==========================================
# math: para funciones matemáticas básicas (exponencial)
# scipy.stats: para trabajar con distribuciones de probabilidad
import math
from scipy.stats import binom, poisson, norm


# ==========================================
# DISTRIBUCION BINOMIAL
# ==========================================
# Modela el número de éxitos en n ensayos con probabilidad p

def binomial_prob(n, p, k):
    # Probabilidad exacta P(X = k)
    return binom.pmf(k, n, p)

def binomial_acumulada(n, p, k):
    # Probabilidad acumulada P(X <= k)
    return binom.cdf(k, n, p)

def binomial_complemento(n, p, k):
    # Probabilidad complemento P(X > k)
    return 1 - binom.cdf(k, n, p)


# ==========================================
# DISTRIBUCION POISSON
# ==========================================
# Modela el número de eventos en un intervalo con tasa promedio lambda

def poisson_prob(lam, k):
    # Probabilidad exacta P(X = k)
    return poisson.pmf(k, lam)

def poisson_acumulada(lam, k):
    # Probabilidad acumulada P(X <= k)
    return poisson.cdf(k, lam)

def poisson_complemento(lam, k):
    # Probabilidad complemento P(X > k)
    return 1 - poisson.cdf(k, lam)


# ==========================================
# DISTRIBUCION NORMAL
# ==========================================
# Se trabaja con la normal estándar usando Z

def normal_prob(z):
    # Probabilidad acumulada P(Z <= z)
    return norm.cdf(z)

def normal_intervalo(a, b):
    # Probabilidad en un intervalo P(a < Z < b)
    return norm.cdf(b) - norm.cdf(a)

def normal_estandarizar(x, mu, sigma):
    # Convierte X a Z usando la fórmula
    return (x - mu) / sigma


# ==========================================
# DISTRIBUCION EXPONENCIAL
# ==========================================
# Modela tiempos de espera entre eventos

def exp_menor(lam, x):
    # Probabilidad P(X < x)
    return 1 - math.exp(-lam * x)

def exp_mayor(lam, x):
    # Probabilidad P(X > x)
    return math.exp(-lam * x)

def exp_intervalo(lam, a, b):
    # Probabilidad P(a < X < b)
    return math.exp(-lam * a) - math.exp(-lam * b)


# ==========================================
# RESULTADOS CON ENUNCIADOS
# ==========================================

print("===== BINOMIAL =====")

# Ejercicio 1:
# Sea X ~ B(10, 0.3)
# Calcular P(X=3) y P(X<=2)
print("\nEjercicio 1: X ~ B(10, 0.3)")
print("P(X=3):", round(binomial_prob(10, 0.3, 3), 4))
print("P(X<=2):", round(binomial_acumulada(10, 0.3, 2), 4))

# Ejercicio 2:
# Sea X ~ B(8, 0.5)
# Calcular P(X=4) y P(X>=6)
print("\nEjercicio 2: X ~ B(8, 0.5)")
print("P(X=4):", round(binomial_prob(8, 0.5, 4), 4))
print("P(X>=6):", round(binomial_complemento(8, 0.5, 5), 4))

# Aplicación:
# Control de calidad: X ~ B(15, 0.1)
print("\nAplicación: X ~ B(15, 0.1)")
print("P(X=2):", round(binomial_prob(15, 0.1, 2), 4))
print("P(X<=1):", round(binomial_acumulada(15, 0.1, 1), 4))


print("\n===== POISSON =====")

# Ejercicio 1:
# X ~ Pois(3)
print("\nEjercicio 1: X ~ Pois(3)")
print("P(X=2):", round(poisson_prob(3, 2), 4))
print("P(X<=1):", round(poisson_acumulada(3, 1), 4))

# Ejercicio 2:
# X ~ Pois(5)
print("\nEjercicio 2: X ~ Pois(5)")
print("P(X=0):", round(poisson_prob(5, 0), 4))
print("P(X>=2):", round(poisson_complemento(5, 1), 4))

# Aplicación:
# Llegadas de clientes: X ~ Pois(4)
print("\nAplicación: X ~ Pois(4)")
print("P(X=3):", round(poisson_prob(4, 3), 4))
print("P(X>5):", round(poisson_complemento(4, 5), 4))


print("\n===== NORMAL =====")

# Ejercicio 1:
# Z ~ N(0,1)
print("\nEjercicio 1: Z ~ N(0,1)")
print("P(Z<1.5):", round(normal_prob(1.5), 4))
print("P(-1<Z<2):", round(normal_intervalo(-1, 2), 4))

# Ejercicio 2:
# X ~ N(70, 10^2)
print("\nEjercicio 2: X ~ N(70, 10^2)")
z1 = normal_estandarizar(80, 70, 10)
print("P(X>80):", round(1 - normal_prob(z1), 4))

z2 = normal_estandarizar(60, 70, 10)
z3 = normal_estandarizar(85, 70, 10)
print("P(60<X<85):", round(normal_intervalo(z2, z3), 4))


print("\n===== EXPONENCIAL =====")

# Ejercicio 1:
# X ~ Exp(2)
print("\nEjercicio 1: X ~ Exp(2)")
print("P(X<1):", round(exp_menor(2, 1), 4))
print("P(X>2):", round(exp_mayor(2, 2), 4))

# Ejercicio 2:
# X ~ Exp(0.5)
print("\nEjercicio 2: X ~ Exp(0.5)")
print("P(1<X<3):", round(exp_intervalo(0.5, 1, 3), 4))

# Aplicación:
# Tiempo de atención: X ~ Exp(3)
print("\nAplicación: X ~ Exp(3)")
print("P(X<0.5):", round(exp_menor(3, 0.5), 4))
print("P(X>1):", round(exp_mayor(3, 1), 4))