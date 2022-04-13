import System.Environment 
import System.Console.Terminfo (enterStandoutMode)
import Text.XHtml (sub)
import Data.ByteString (sort)
import Data.List (sortBy)

-- a week has 5 days and every day consists of ten 1 hour slots (8:00-18:00)
type SchoolTimetable = [ClassTimetable]
type ClassTimetable = [Slot]
data Slot = Lesson Teacher Subject Room | Free
instance Show Slot where 
    show Free = ""
    show (Lesson teacher subject room) = teacher ++ ", " ++ subject ++ ", " ++ room
type Teacher = String
type Subject = String
type Room = String

-- first argument is num_entities, second is num_generations
main = do
    args <- getArgs  
    print (show (run (map read args)))

run :: [Int] -> SchoolTimetable
run [numEnts, numGens] = head (sortTimetables iterationRes)
    where iterationRes = Main.iterate numGens (generateInitialEnts numEnts)
run _ = error "incorrect number of command line arguments"

-- helper function
sortTimetables :: [SchoolTimetable] -> [SchoolTimetable]
sortTimetables = sortBy (\x y -> if fitness x > fitness y then GT else if fitness x == fitness y then EQ else LT)

-- TODO
fitness :: SchoolTimetable -> Int 
fitness ent = 0

iterate :: Int -> [SchoolTimetable] -> [SchoolTimetable]
iterate 0 ents = ents
iterate n currEnts = Main.iterate (n-1) newEnts
    where 
        newEnts = crossOver mutatedEnts
        mutatedEnts = map mutate currEnts

-- TODO
crossOver :: [SchoolTimetable] -> [SchoolTimetable]
crossOver ents = ents

-- TODO
mutate :: SchoolTimetable -> SchoolTimetable
mutate ent = ent

-- TODO
generateInitialEnts :: Int -> [SchoolTimetable]
generateInitialEnts n = []