import System.Environment
import Data.List (sortBy)
-- import System.Random

-- types that represent the requirements
type TeacherToSubjects = (String, [String])
type ClassToSubjectHours = (String, [(String, Int)])
type Requirements = ([TeacherToSubjects], [ClassToSubjectHours])

-- types that represent the timetable
-- a week has 5 days and every school-day consists of ten 1 hour slots (8:00-18:00)
type SchoolTimetable = [ClassTimetable]
type ClassTimetable = [Slot]
data Slot = Lesson Teacher Subject | Free
instance Show Slot where
    show Free = " FREE"
    show (Lesson teacher subject) = " LESSON: " ++ teacher ++ " - " ++ subject
type Teacher = String
type Subject = String

main = do
    let requirements = ([("Mr Wirz", ["Math"]),("Mrs Rosenberg", ["Biology", "Design Of Digital Circuits"]),("Mr Erlacher", ["Swiss-German"])],[("1A",[("Math", 4), ("Biology", 1), ("Swiss-German", 2)]),("1B", [("Math", 3), ("Biology", 3), ("Swiss-German", 1)])])
    -- READABLE VERSION: 
    -- (
    --     [
    --         ("Mr Wirz", ["Math"]),
    --         ("Mrs Rosenberg", ["Biology", "Design Of Digital Circuits"]), 
    --         ("Mr Erlacher", ["Swiss-German"])
    --     ], 
    --     [
    --         (
    --             "1A",
    --             [("Math", 4), ("Biology", 1), ("Swiss-German", 2)]
    --         ),
    --         (
    --             "1B", 
    --             [("Math", 3), ("Biology", 3), ("Swiss-German", 1)]
    --         )
    --     ]
    -- )
    print (show (run 100 10 0.1 requirements)) 
    -- PARAMETERS: 
    -- 1st = number of entities per generation
    -- 2nd = number of generations (= iteration of the algorithm) 
    -- 3rd = percentage of how many ents in the next gen should come from the top ents of the last gen
    

run :: Int -> Int -> Float -> Requirements -> SchoolTimetable
run numEnts numGens elitismDegree reqs = head (sortTimetables iterationRes)
    where iterationRes = Main.iterate numEnts numGens elitismDegree (generateInitialEnts numEnts reqs)

-- little helper function: sort a list of school timetables by fitness
sortTimetables :: [SchoolTimetable] -> [SchoolTimetable]
sortTimetables = sortBy (\x y -> if fitness x > fitness y then GT else if fitness x == fitness y then EQ else LT)

fitness :: SchoolTimetable -> Int
fitness table = if score == 0 then actualFitness table else (- score)
    where
        score = invalidityScore table

-- TODO: implement the fitness function of the algorithm 
actualFitness :: SchoolTimetable -> Int
actualFitness table = 0

-- TODO: return a score of how badly invalid a given timetable is (or 0 if it's valid)
invalidityScore :: SchoolTimetable -> Int
invalidityScore _ = 0

iterate :: Int -> Int -> Float -> [SchoolTimetable] -> [SchoolTimetable]
iterate 0 numEnts elitismDegree currEnts = currEnts
iterate n numEnts elitismDegree currEnts = lastGenElites ++ nextGenSurvivors
    where
        elitismNumber = floor (fromIntegral numEnts * elitismDegree)
        lastGenElites = take elitismNumber (sortTimetables currEnts)
        mutatedEnts = map mutate currEnts
        newEnts = crossOver mutatedEnts
        nextGen = Main.iterate (n-1) numEnts elitismDegree newEnts
        nextGenSurvivors = take (numEnts - elitismNumber) (sortTimetables nextGen)

-- TODO: perform all the crossing overs that should happen in a generation
crossOver :: [SchoolTimetable] -> [SchoolTimetable]
crossOver ents = ents

-- very simple implementation: a mutation is just swapping two slots in the timetable of a class
mutate :: SchoolTimetable -> SchoolTimetable
mutate = map (performMuts numMuts)
    where
        numMuts = 0 -- randomRIO (0, 5)

-- perform all the mutations that a class timetable should recieve
performMuts :: Int -> ClassTimetable -> ClassTimetable
performMuts 0 table = table
performMuts n table = performMuts (n - 1) (performSingleMut table)
    
performSingleMut :: ClassTimetable -> ClassTimetable
performSingleMut = swap ind1 ind2 
    where 
        ind1 = 0 --randomRIO (0, 49)
        ind2 = 0 --randomRIO (0, 49)

-- swaps out the two list elements specified by ind1 and ind2
swap :: Int -> Int -> [a] -> [a]
swap ind1 ind2 table = firstPart ++ [table !! ind2] ++ middlePart ++ [table !! ind1] ++ endPart
    where
        firstPart = take ind1 table
        middlePart = drop (ind1 + 1) (take ind2 table)
        endPart = drop (ind2 + 1) table

-- very simple implementation: construct initial tables based on ClassToSubjectHours only and if one of them ends up being invalid 
-- (e.g. a teacher teaching 2 classes at the same time) it'll just get a negative fitness score (and will hence get eliminated soon).
-- if this implementation is too slow (which it probably will) we could run FET for a short time (say 20 seconds) and hope that that
-- generates a reasonable starting point which we can then refine with the genetic procedure
generateInitialEnts :: Int -> Requirements -> [SchoolTimetable]
generateInitialEnts 0 _ = []
generateInitialEnts n reqs = generateInitialEnt reqs : generateInitialEnts (n-1) reqs

-- generates timetable for an enitre school
generateInitialEnt :: Requirements -> SchoolTimetable
generateInitialEnt (teachers, x:xs) = generateInitialTableForClass (snd x) teachers : generateInitialEnt (teachers, xs)
generateInitialEnt _ = []

-- generated a timetable for a given class
generateInitialTableForClass :: [(String, Int)] -> [TeacherToSubjects] -> ClassTimetable
generateInitialTableForClass subjHourList teachers = subjectSlots ++ paddingSlots (50 - length subjectSlots)
    where subjectSlots = foldr (\info list -> generateSlots info teachers ++ list) [] subjHourList

-- generates a list of slots for a given subject
generateSlots :: (String, Int) -> [TeacherToSubjects] -> [Slot]
generateSlots (_, 0) _ = []
generateSlots (subj, n) teachers = Lesson (findTeacherForSubject subj teachers) subj : generateSlots (subj, n - 1) teachers

-- generates as many free Slots as are needed to fill a school-week (= 50 hours)
paddingSlots :: Int -> [Slot]
paddingSlots 0 = []
paddingSlots n = Free : paddingSlots (n - 1)

-- implementation assumes that there exists at least one teacher for each subjet
findTeacherForSubject :: String -> [TeacherToSubjects] -> String
findTeacherForSubject subject teachers =
    head (foldr (\(name, hisSubjects) list -> if subject `elem` hisSubjects then name : list else list) [] teachers)