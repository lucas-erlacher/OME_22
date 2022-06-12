# Optimizing school timetables with genetic algorithms

# TODOs
(number indicates priority)
## (1) Benchmark setups of old/new mutation with/wo crossover and decide which ones are effective
## (2) Check wether precalculating fitness before sorting improves it. 
Laurent suspects it might not memo the result and calculates fitness nlogn times.

Question (by Lucas): fitness is never computed more than once for the same ent (bc of that fitness_cache dict in the fitness method). Ich verstehe nicht ganz was fitnesses vor dem sortieren vorberechnen bringen würde. Aber kann auch gut sein dass ich etwas übersehe ! 
## (3) Make mutation concentrate on unfit slots and classes
We mostly replace fit slots, which is not likely to improve the tables. This could be done by defining a slot- and class-local notion of fitness

Implemented fit_slots_mut_rate parameter which kind of does something like this. This made the evolution in the initial 100 or so generations even faster, however over the long run (1000 or so generations) using this feature made no difference. 
## (3) Parametrize/diversify selection process
ideas:
### Make unfit tables mutate/crossover harder
### Check fitness change every iteration and stop if it stagnates
## (3) Check wether we can avoid some ent deepcopies
Maybe try to do elitism in place or smth. Might not be possible.
## (4) Testcases
The current testcase is highly structured (not very reaslistic). Write more testcases or code that generates testscases. 
Also, write code that determines the theoretically optimal fitness value of a given test case (so that we can in the end compare the reusult of our algo to that optimum). 
## (6) Type more expressions. give names to fields of ents etc

# Benchmark results

| commit_date | c | ents | its | mr   | fit_mr | el  | tm | cm | cmc | fit |
|-------------|---|------|-----|------|--------|-----|----|----|-----|-----|
| 2022-05-29  | n | 20   | 150 | 0.75 | 1      | 0.5 | 50 | 30 | 1   | 676 |
| 2022-06-06  | n | 100  | 1500| 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 721 |
| 2022-06-06  | y | 100  | 500 | 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 716 |
| 2022-06-06  | y | 100  | 1000| 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 728 |
| 2022-06-06  | y | 100  | 1500| 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 740 |
| 2022-06-12  | y | 100  | 1500| 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 767 |
| 2022-06-12  | y | 100  | 1500| 0.9  | 1      | 0.75| 60 | 10 | 0.4 | 767 |

legend:
- c : crossover?
- mr : mutation rate
- el : elitism degree
- tm : Average amount of teacher placements to be mutated per iteration
- cm : Average amount of course<->class<->slot bindings to be mutated per iteration
- cmc: course mutation chance
- fit_mr: mutation rate for slots that are already quite fit
