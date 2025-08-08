
import pandas as pd
import random

def load_imams(filepath="imams.csv"):
    df = pd.read_csv(filepath)
    imam_data = []
    for _, row in df.iterrows():
        imam_data.append({
            "nama": row["Nama"],
            "hari": row["Hari"].split(","),
            "kapasitas": int(row["Kapasitas"])
        })
    return imam_data

def generate_individual(total_slots, imams):
    return [random.choice(imams)["nama"] for _ in range(total_slots)]

def evaluate(individual, imams, hari_list, shalat_list):
    tugas_per_imam = {imam["nama"]: 0 for imam in imams}
    score = 0
    for i, imam_name in enumerate(individual):
        hari = hari_list[i // len(shalat_list)]
        imam = next((x for x in imams if x["nama"] == imam_name), None)
        if imam and hari in imam["hari"] and tugas_per_imam[imam_name] < imam["kapasitas"]:
            score += 1
        tugas_per_imam[imam_name] += 1
    return score

def selection(population, imams, hari_list, shalat_list):
    return sorted(population, key=lambda x: evaluate(x, imams, hari_list, shalat_list), reverse=True)[:2]

def crossover(p1, p2, rate):
    if random.random() > rate:
        return p1[:], p2[:]
    point = random.randint(1, len(p1)-2)
    c1 = p1[:point] + [x for x in p2 if x not in p1[:point]]
    c2 = p2[:point] + [x for x in p1 if x not in p2[:point]]
    return c1, c2

def mutate(ind, rate, imams):
    for i in range(len(ind)):
        if random.random() < rate:
            ind[i] = random.choice(imams)["nama"]
    return ind

def run_ga(pop_size, n_gen, crossover_rate, mutation_rate, imams):
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    shalat_list = ["Subuh", "Dzuhur", "Ashar", "Maghrib", "Isya"]
    total_slots = len(hari_list) * len(shalat_list)

    population = [generate_individual(total_slots, imams) for _ in range(pop_size)]
    fitness_history = []

    for _ in range(n_gen):
        new_pop = []
        selected = selection(population, imams, hari_list, shalat_list)
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(selected, 2)
            c1, c2 = crossover(p1, p2, crossover_rate)
            new_pop.append(mutate(c1, mutation_rate, imams))
            if len(new_pop) < pop_size:
                new_pop.append(mutate(c2, mutation_rate, imams))
        population = new_pop
        best = max(population, key=lambda x: evaluate(x, imams, hari_list, shalat_list))
        fitness_history.append(evaluate(best, imams, hari_list, shalat_list))

    best = max(population, key=lambda x: evaluate(x, imams, hari_list, shalat_list))
    return best, evaluate(best, imams, hari_list, shalat_list), fitness_history, hari_list, shalat_list
