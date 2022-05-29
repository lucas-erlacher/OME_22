# Optimizing school timetables with genetic algorithms

# TODOs
(number indicates priority)
## (1) Benchmark setups of old/new mutation with/wo crossover and decide which ones are effective
## (2) Check wether precalculating fitness before sorting improves it. 
Laurent suspects it might not memo the result and calculates fitness nlogn times.
## (3) Make mutation concentrate on unfit slots and classes
We mostly replace fit slots, which is not likely to improve the tables. This could be done by defining a slot- and class-local notion of fitness
## (3) Parametrize/diversify selection process
ideas:
### Make unfit tables mutate/crossover harder
### Check fitness change every iteration and stop if it stagnates
## (3) Check wether we can avoid some ent deepcopies
Maybe try to do elitism in place or smth. Might not be possible.
## (3) Rethink crossover
In order to get more performant implementation, possibly by fixing teacher conflicts more efficiently. Slot-specific fixing is implemented in teacher refilling in mutation 
## (5) Type more expressions. give names to fields of ents etc
