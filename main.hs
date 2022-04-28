import Data.List (sortBy, nub, delete)
import Data.Time.Clock.POSIX
import System.IO.Unsafe

-- ################################################################################################################################
-- TYPE DEFINITIONS

-- types that represent the requirements of a school
type TeacherToSubjects = (String, [String])
type ClassToSubjectHours = (String, [(String, Int)])
type Requirements = ([TeacherToSubjects], [ClassToSubjectHours])

-- types that represent the timetable (of a school-week and of a class-week)
-- a week has 5 days and every school-day consists of ten 1 hour slots (8:00-18:00)
type SchoolTimetable = [ClassTimetable]
type ClassTimetable = [Slot]
data Slot = Lesson Teacher Subject | Free
instance Show Slot where
    show Free = " FREE"
    show (Lesson teacher subject) = " LESSON: " ++ teacher ++ " - " ++ subject
instance Eq Slot where  
    (==) Free Free = True
    (==) Free (Lesson _ _) = False
    (==) (Lesson _ _) Free = False
    (==) (Lesson t1 s1) (Lesson t2 s2) = (t1 == t2) && (s1 == s2)
type Teacher = String
type Subject = String
-- ################################################################################################################################




-- ################################################################################################################################
-- MAIN FUNCTION AND MAIN LOOP

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

    print (show (run 100 20 5 0.2 requirements)) 
    -- PARAMETERS: 
    -- 1st = number of entities per generation (needs to be even for current implementation of crossOver)
    -- 2nd = number of generations (= iterations of the algorithm) 
    -- 3rd = number of mutations that every entity should recieve in a generation
    -- 4th = percentage of how many next gen ents should come from the top ents of the last gen
    
run :: Int -> Int -> Int -> Float -> Requirements -> SchoolTimetable
run numEnts numGens numMuts elitismDegree reqs = head (sortTimetables iterationRes)
    where iterationRes = Main.iterate numEnts numGens numMuts elitismDegree (generateInitialEnts numEnts reqs)

-- main loop of the program (which runs numGens many times)
iterate :: Int -> Int -> Int -> Float -> [SchoolTimetable] -> [SchoolTimetable]
iterate _ 0  _ _ currEnts = currEnts
iterate numEnts n numMuts elitismDegree currEnts = lastGenSurvivors ++ nextGenSurvivors
    where
        elitismNumber = floor (fromIntegral numEnts * elitismDegree)
        lastGenSurvivors = take elitismNumber (sortTimetables currEnts)
        mutatedEnts = map (mutate numMuts) currEnts
        newEnts = crossOver mutatedEnts
        nextGen = Main.iterate numEnts (n-1) numMuts elitismDegree newEnts
        nextGenSurvivors = take (numEnts - elitismNumber) (sortTimetables nextGen)
-- ################################################################################################################################




-- ################################################################################################################################
-- FITNESS FUNCTION

-- checks whether the table is invalid (in which case it'll get a negative score) and if it's not computes it's actual fitness value
fitness :: SchoolTimetable -> Int
fitness table = if score == 0 then actualFitness table else (- score)
    where
        score = invalidityScore table

-- TODO: implement the actual fitness function of the algorithm 
actualFitness :: SchoolTimetable -> Int
actualFitness table = 0

-- TODO: return a score of how badly invalid a given timetable is (or 0 if it's valid)
invalidityScore :: SchoolTimetable -> Int
invalidityScore _ = 0
-- ################################################################################################################################




-- ################################################################################################################################
-- CROSSING OVER

-- creates pairs of ents and crosses over the two ents from a pair
-- assumes that there is an even number of entities in the generation
crossOver :: [SchoolTimetable] -> [SchoolTimetable]
crossOver [] = []
crossOver oldEnts = (performSingleCrossOver candidates) ++ (crossOver oldEntsRest)
    where 
        candidates = candidate1 : (candidate2 : [])
        spot1 = getRandomInt ((length oldEnts) - 1)
        candidate1 = oldEnts !! spot1 
        firstCandRemoved = (delete candidate1 oldEnts)
        spot2 = getRandomInt ((length firstCandRemoved) - 1)
        candidate2 = firstCandRemoved !! spot2
        oldEntsRest = (delete candidate2 firstCandRemoved)

-- TODO: performs crossing over on a pair of SchoolTimetables (resulting in two new SchoolTimetables). 
performSingleCrossOver :: [SchoolTimetable] -> [SchoolTimetable]
performSingleCrossOver ents = ents
-- ################################################################################################################################




-- ################################################################################################################################
-- MUTATION

-- very simple implementation: a mutation is just swapping two slots in the timetable of a class
mutate :: Int -> SchoolTimetable -> SchoolTimetable
mutate numMuts = map (performMuts numMuts)

-- perform all the mutations that a class timetable should recieve
performMuts :: Int -> ClassTimetable -> ClassTimetable
performMuts 0 table = table
performMuts n table = performMuts (n - 1) (performSingleMut table)
    
performSingleMut :: ClassTimetable -> ClassTimetable
performSingleMut = swap ind1 ind2 
    where 
        ind1 = getRandomInt 49
        ind2 = getRandomInt 49

-- swaps out the two list elements specified by ind1 and ind2
swap :: Int -> Int -> [a] -> [a]
swap ind1 ind2 table = firstPart ++ [table !! ind2] ++ middlePart ++ [table !! ind1] ++ endPart
    where
        firstPart = take ind1 table
        middlePart = drop (ind1 + 1) (take ind2 table)
        endPart = drop (ind2 + 1) table
-- ################################################################################################################################




-- ################################################################################################################################
-- GENERATION OF INTIAL ENTITIES

-- very simple implementation: construct initial tables based on ClassToSubjectHours only and if one of them ends up being invalid 
-- (e.g. a teacher teaching 2 classes at the same time) it'll just get a negative fitness score (and will hence get eliminated soon).
-- if this implementation is too slow (which it probably will) we could run FET for a short time (say 20 seconds) and hope that that
-- generates a reasonable starting point which we can then refine with the genetic procedure. 
generateInitialEnts :: Int -> Requirements -> [SchoolTimetable]
generateInitialEnts 0 _ = []
generateInitialEnts n reqs = generateInitialEnt reqs : generateInitialEnts (n-1) reqs

-- generates timetable for an enitre school
generateInitialEnt :: Requirements -> SchoolTimetable
generateInitialEnt (teachers, x:xs) = generateInitialTableForClass (snd x) teachers : generateInitialEnt (teachers, xs)
generateInitialEnt _ = []

-- generates a timetable for a given class
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
-- ################################################################################################################################




-- ################################################################################################################################
-- HELPER FUNCTIONS 

-- little helper function: sort a list of school timetables by fitness
sortTimetables :: [SchoolTimetable] -> [SchoolTimetable]
sortTimetables = sortBy (\x y -> if fitness x > fitness y then GT else if fitness x == fitness y then EQ else LT)
-- ################################################################################################################################




-- ################################################################################################################################
-- RANDOM NUMBERS 
-- (I have to implement this myself because all of the libraries I tried have compatability issues with my ARM Mac)

-- returns a random integer in [0, first_argument]. 
getRandomInt :: Int -> Int
getRandomInt max = boundedInt + waste_time  -- waste a some time in order to ensure that the next Int will be different
    where
        boundedInt = mod timeAsInt max
        timeAsInt = (unsafePerformIO (round . (1000000 *) <$> getPOSIXTime))
        -- THIS IS WHAT THE DOCUMENTATION SAYS ABOUT unsafePerformIO: 
        -- "For this to be safe, the IO computation should be free of side effects and independent of its environment."
        -- As far as I'm concerned both these criteria are met so I think it should fine to use usafePerformIO here.
        waste_time = ((sum [0..(mod timeAsInt 10000)]) * 0)  -- returns 0 but wastes some time (which is what we want)

getRandomIntList :: Int -> Int -> [Int]
getRandomIntList len max = map (\x -> getRandomInt max) (replicate len 0) 
-- ################################################################################################################################
