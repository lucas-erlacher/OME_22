import System.Environment 
import System.Console.Terminfo (enterStandoutMode)
import Text.XHtml (sub)
import Data.ByteString (sort)
import Data.List (sortBy)
import qualified Data.ByteString.Lazy

type TeacherToSubject = (String, String)
type ClassToSubjectHours = (String, [(String, Int)])
type Requirements = ([TeacherToSubject], [ClassToSubjectHours])

main = do
    let requirements = ([("Mr Wirz", "Math"),("Mrs Rosenberg", "Biology"),("Mr Erlacher", "Swiss-German")],[("1A",[("Math", 4), ("Biology", 1), ("Swiss-German", 2)]),("1B", [("Math", 3), ("Biology", 3), ("Swiss-German", 1)])])
    -- READABLE VERSION: 
    -- (
    --     [
    --         ("Mr Wirz", "Math"),
    --         ("Mrs Rosenberg", "Biology"), 
    --         ("Mr Erlacher", "Swiss-German")
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
    print (show (run 100 10 requirements))

-- a week has 5 days and every day consists of ten 1 hour slots (8:00-18:00)
type SchoolTimetable = [ClassTimetable]
type ClassTimetable = [Slot]
data Slot = Lesson Teacher Subject | Free
instance Show Slot where 
    show Free = "FREE"
    show (Lesson teacher subject) = "LESSON: " ++ teacher ++ ", " ++ subject
type Teacher = String
type Subject = String

run :: Int -> Int -> Requirements -> SchoolTimetable
run numEnts numGens reqs  = head (sortTimetables iterationRes)
    where iterationRes = Main.iterate numGens (generateInitialEnts numEnts reqs)

-- helper function
sortTimetables :: [SchoolTimetable] -> [SchoolTimetable]
sortTimetables = sortBy (\x y -> if fitness x > fitness y then GT else if fitness x == fitness y then EQ else LT)

fitness :: SchoolTimetable -> Int 
fitness table = if score == 0 then actualFitness table else (- score)
    where 
        score = invalidityScore table
        actualFitness table = 0  -- TODO: just a placeholder for now

-- TODO: return a score of how invalid a given timetable is
invalidityScore :: SchoolTimetable -> Int
invalidityScore _ = 0

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

-- very simple implementation: construct initial tables based on ClassToSubjectHours only and if one of them ends up being invalid 
-- (e.g. a teacher teaching 2x at the same time) it'll just get a negative fitness score (and will hence get eliminated soon)
generateInitialEnts :: Int -> Requirements -> [SchoolTimetable]
generateInitialEnts 0 _ = []
generateInitialEnts n reqs = generateInitialEnt reqs : generateInitialEnts (n-1) reqs

generateInitialEnt :: Requirements -> SchoolTimetable
generateInitialEnt (teachers, x:xs) = generateInitialTableForClass (snd x) teachers : generateInitialEnt (teachers, xs) 
generateInitialEnt _ = []
        
generateInitialTableForClass :: [(String, Int)] -> [TeacherToSubject] -> ClassTimetable
generateInitialTableForClass subjHourList teachers = foldr (\info list -> generateSlots info teachers ++ list) [] subjHourList

generateSlots :: (String, Int) -> [TeacherToSubject] -> [Slot]
generateSlots (_, 0) _ = []
generateSlots (subj, n) teachers = Lesson (findTeacherForSubject subj teachers) subj : generateSlots (subj, n - 1) teachers

-- implementation assumes that there exists at least one teacher for each subjet
findTeacherForSubject :: String -> [TeacherToSubject] -> String
findTeacherForSubject subject teachers = 
    head (foldr (\(name, hisSubject) list -> if hisSubject == subject then name : list else list) [] teachers)