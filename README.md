# Optimizing school timetables with genetic algorithms

# current state:


# TODOs
(number indicates priority)
## (0) Fix crossover
It currently somehow adds additional subjects(removing free slots) in the last class. See the freeslots statement. That's probably why it helps so much :) closes gaps and adds more prefered subjects :)
## (1) Benchmark setups of old/new mutation with/wo crossover and decide which ones are effective
## (2) Check wether precalculating fitness before sorting improves it. 
Laurent suspects it might not memo the result and calculates fitness nlogn times.

Question (by Lucas): fitness is never computed more than once for the same ent (bc of that fitness_cache dict in the fitness method). Ich verstehe nicht ganz was fitnesses vor dem sortieren vorberechnen bringen würde. Aber kann auch gut sein dass ich etwas übersehe ! 
## (3) Make mutation concentrate on unfit slots and classes
We mostly replace fit slots, which is not likely to improve the tables. This could be done by defining a slot- and class-local notion of fitness
## (3) Parametrize/diversify selection process
ideas:
### Make unfit tables mutate/crossover harder
### Check fitness change every iteration and stop if it stagnates
## (3) Check wether we can avoid some ent deepcopies
Maybe try to do elitism in place or smth. Might not be possible.
## (5) Type more expressions. give names to fields of ents etc

# Benchmark results

| commit_date | c | ents | its | mr   | el  | tm | cm | cmc | fit |
|-------------|---|------|-----|------|-----|----|----|-----|-----|
| 2022-05-29  | n | 20   | 150 | 0.75 | 0.5 | 50 | 30 | 1   | 676 |
| 2022-06-06  | n | 100  | 1500| 0.9  | 0.75| 60 | 10 | 0.4 | 721 |
| 2022-06-06  | y | 100  | 500 | 0.9  | 0.75| 60 | 10 | 0.4 | 727 |

legend:
- c : crossover?
- mr : mutation rate
- el : elitism degree
- tm : Average amount of teacher placements to be mutated per iteration
- cm : Average amount of course<->class<->slot bindings to be mutated per iteration
- cmc: course mutation chance
