import random
import numpy as np

depoSayisi = 0
musteriSayisi = 0

depoKapasiteleri = []
depolarinKurulumMaliyetleri = []
musteriTalepleri = []
musteriDepoMaliyetleri = []

with open('wl_500_3', 'r') as file:
    d, m = map(int, file.readline().split())
    depoSayisi = d
    musteriSayisi = m

    pairs = []
    for _ in range(d):
        pair = tuple(map(float, file.readline().split()))
        pairs.append(pair)
    depoKapasiteleri = [pair[0] for pair in pairs]
    depolarinKurulumMaliyetleri = [pair[1] for pair in pairs]

    for i in range(m):
        num = int(file.readline())
        musteriTalepleri.append(num)
        floats = list(map(float, file.readline().split()))
        musteriDepoMaliyetleri.append(floats)

population_size = 100 #Genetik Algoritmayla oluşturulan çözümlerin toplam sayısı
max_generations = 300 #300 jenerasyonla çalışacağı belirtilir
mutation_rate = 0.07  #Mutasyona uğrama olasılığı. Bu üç parametre için farklı farklı değerler denedim en iyisinin bu değerler olduğuna kanaat getirdim.

def generate_individual():
    return [random.randint(0, depoSayisi-1) for _ in range(musteriSayisi)]

population = [generate_individual() for _ in range(population_size)]

def evaluate_fitness(individual):
    total_cost = sum(depolarinKurulumMaliyetleri[i] for i in set(individual))
    for j in range(depoSayisi):
        depoVerilenMusteriler = [i for i in range(musteriSayisi) if individual[i] == j]
        total_cost += sum(musteriDepoMaliyetleri[i][j] for i in depoVerilenMusteriler)
        total_demand = sum(musteriTalepleri[i] for i in depoVerilenMusteriler)
        if total_demand > depoKapasiteleri[j]:
            total_cost += (total_demand - depoKapasiteleri[j]) * 1000
    return total_cost

def selection(population):
    return random.choice(population)

def crossover(parent1, parent2):
    crossover_point = random.randint(1, musteriSayisi - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(individual):
    for i in range(musteriSayisi):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, depoSayisi - 1)
    return individual

best_fitness = float('inf')
best_solution = None

for generation in range(max_generations):
    fitness_values = [evaluate_fitness(individual) for individual in population]

    min_fitness = min(fitness_values)
    min_index = np.argmin(fitness_values)
    if min_fitness < best_fitness:
        best_fitness = min_fitness
        best_solution = population[min_index]
    new_population = []

    while len(new_population) < population_size:
        parent1 = selection(population)
        parent2 = selection(population)

        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1)
        child2 = mutation(child2)

        new_population.append(child1)
        new_population.append(child2)

    population = new_population

print("Optimal Maliyet:", best_fitness)
print("Müşterilere Atanan Depolar: "," ".join(str(i) for i in best_solution))