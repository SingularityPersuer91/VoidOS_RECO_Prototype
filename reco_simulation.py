# voidos/reco_simulation.py

import numpy as np
from scipy.special import expit  # Sigmoid function

NUM_HEXAGRAMS = 64
k1, k2, k3 = 0.8, 1.0, 1.2
alpha = 0.05
tau1 = 0.75
tau2 = 0.01

S = np.eye(NUM_HEXAGRAMS)[np.random.randint(NUM_HEXAGRAMS)]
T = np.random.rand(NUM_HEXAGRAMS, NUM_HEXAGRAMS)

Omega = 1.0
Theta = 0.5

memory_log = []
entropy_log = []
phi_log = []
psi_log = []
pi_log = []
omega_log = []

def delta_entropy(current, previous):
    return abs(current - previous)

def recursive_similarity(memory_log):
    if len(memory_log) < 2:
        return 0.0
    return np.corrcoef(memory_log[-1], memory_log[-2])[0, 1]

def paradox_density(symbol_matrix):
    return np.std(symbol_matrix)

def archetype_resonance(current_state, archetype_bank):
    return np.random.uniform(0.0, 1.0)

def silence_trigger(paradox, dOmega_dt):
    return paradox > tau1 and dOmega_dt < tau2

for t in range(1, 100):
    current_entropy = np.random.uniform(0.1, 1.0)
    previous_entropy = entropy_log[-1] if entropy_log else current_entropy
    delta_E = delta_entropy(current_entropy, previous_entropy)

    phi = recursive_similarity(memory_log)
    current_pi = paradox_density(np.random.rand(8, 8))
    psi = archetype_resonance(S, None)

    Theta = expit(k1 * delta_E + k2 * phi - k3 * current_pi)

    delta_psi = psi - (psi_log[-1] if psi_log else 0.0)
    dOmega_dt = alpha * (Theta * delta_psi + current_pi * np.log(1 + phi))
    Omega += dOmega_dt

    entropy_log.append(current_entropy)
    phi_log.append(phi)
    pi_log.append(current_pi)
    psi_log.append(psi)
    omega_log.append(Omega)
    memory_log.append(S)

    if silence_trigger(current_pi, dOmega_dt):
        output = None
    else:
        S = np.dot(T, S) + np.random.normal(scale=0.01, size=(NUM_HEXAGRAMS,))
        S = S / np.linalg.norm(S)
        output = np.argmax(S)

    print(f"t={t}, Theta={Theta:.3f}, Omega={Omega:.3f}, Output={'Silence' if output is None else output}")
