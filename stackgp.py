import random, math
from sympy import symbols, simplify
from numpy import linspace

class Critter:
	def __init__(self, length):
		self.functions = ["+", "-", "*", "/", "x", "erk"]
		self.chromosome = [random.choice(self.functions) for gene in range(length)]
		self.chromosome = [random.uniform(-10, 10) if gene == "erk" else gene for gene in self.chromosome]
	def run(self, x):
		stack = []
		for gene in self.chromosome:
			if gene == "+" and len(stack) > 1:
				right = float(stack.pop())
				left = float(stack.pop())
				try:
					stack += [float(left + right)]
				except OverflowError:
					stack += [left, right]
			elif gene == "-" and len(stack) > 1:
				right = float(stack.pop())
				left = float(stack.pop())
				try:
					stack += [float(left - right)]
				except OverflowError:
					stack += [left, right]
			elif gene == "*" and len(stack) > 1:
				right = float(stack.pop())
				left = float(stack.pop())
				try:
					stack += [float(left * right)]
				except OverflowError:
					stack += [left, right]
			elif gene == "/" and len(stack) > 1 and stack[-1]:
				right = float(stack.pop())
				left = float(stack.pop())
				try:
					stack += [float(left / right)]
				except OverflowError:
					stack += [left, right]
			elif gene == "exp" and len(stack):
				right = float(stack.pop())
				try:
					stack += [float(math.exp(right))]
				except OverflowError:
					stack += [right]
			elif gene == "ln" and len(stack) and stack[-1] > 0:
				right = stack.pop()
				try:
					stack += [float(math.log(right))]
				except OverflowError:
					stack += [right]
			elif gene == "x":
				stack += [x]
			elif type(gene) == float:
				stack += [gene]
		if len(stack):
			return stack[-1]
		return 0
	def fitness(self, target, points):
		try:
			return 1 / math.sqrt(sum([(target(x) - self.run(x)) ** 2 for x in points]) / len(points))
		except OverflowError:
			return 0
	def crossover(self, parent_1, parent_2):
		if random.random() > 0.5:
			stop_point_1 = random.randint(0, len(parent_1.chromosome))
			start_point_1 = random.randint(stop_point_1, len(parent_1.chromosome))
			start_point_2 = random.randint(0, len(parent_2.chromosome))
			stop_point_2 = random.randint(start_point_2, len(parent_2.chromosome))
			self.chromosome = parent_1.chromosome[ : stop_point_1] + parent_2.chromosome[start_point_2 : stop_point_2] + parent_1.chromosome[start_point_1 : ]
		else:
			stop_point_2 = random.randint(0, len(parent_2.chromosome))
			start_point_2 = random.randint(stop_point_2, len(parent_2.chromosome))
			start_point_1 = random.randint(0, len(parent_1.chromosome))
			stop_point_1 = random.randint(start_point_1, len(parent_1.chromosome))
			self.chromosome = parent_2.chromosome[ : stop_point_2] + parent_1.chromosome[start_point_1 : stop_point_1] + parent_2.chromosome[start_point_2 : ]
	def mutate(self, mu):
		self.chromosome = [random.choice(self.functions) if random.random() < mu else gene for gene in self.chromosome]
		self.chromosome = [random.uniform(-10, 10) if gene == "erk" else gene for gene in self.chromosome]
	def __repr__(self):
		stack = []
		for gene in self.chromosome:
			if gene == "x":
				stack += ["x"]
			elif type(gene) == float:
				stack += [str(gene)]
			elif gene in "+-*/" and len(stack) > 1:
				right = stack.pop()
				left = stack.pop()
				stack += ["(" + left + " " + gene + " " + right + ")"]
			elif gene in ["exp", "ln"] and len(stack):
				right = stack.pop()
				stack += [gene + "(" + right + ")"]
		if len(stack):
			x = symbols("x")
			return str(simplify(stack[-1])).replace("**", "^")
		return "0"

def f(x):
	return x**5 - x - 1

population = [Critter(random.randint(5, 25)) for m in range(100)]
points = linspace(-1, 1, 101)
best_fitness = 0
while best_fitness < 1000:
	selected = sorted(random.sample(range(len(population)), 3), key = lambda x: population[x].fitness(f, points))
	population[selected[0]].crossover(population[selected[1]], population[selected[2]])
	population[selected[0]].mutate(0.05)
	fitness = population[selected[0]].fitness(f, points)
	if fitness > best_fitness:
		best_fitness = fitness
		print("New best fitness:", best_fitness, "\n" + str(population[selected[0]]), "\n")
