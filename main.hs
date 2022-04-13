import System.Environment 
import System.Console.Terminfo (enterStandoutMode)
import Text.XHtml (sub)
import Data.ByteString (sort)
import Data.List (sortBy)
import qualified Data.ByteString.Lazy

type TeacherToSubject = (String, String)
type ClassToSbjectHours = (String, [(String, Int)])
type Requirements = ([TeacherToSubject], [ClassToSbjectHours])

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
data Slot = Lesson Teacher Subject Room | Free
instance Show Slot where 
    show Free = ""
    show (Lesson teacher subject room) = teacher ++ ", " ++ subject ++ ", " ++ room
type Teacher = String
type Subject = String
type Room = String

run :: Int -> Int -> Requirements -> SchoolTimetable
run numEnts numGens reqs  = head (sortTimetables iterationRes)
    where iterationRes = Main.iterate numGens (generateInitialEnts numEnts reqs)

-- helper function
sortTimetables :: [SchoolTimetable] -> [SchoolTimetable]
sortTimetables = sortBy (\x y -> if fitness x > fitness y then GT else if fitness x == fitness y then EQ else LT)

-- TODO
fitness :: SchoolTimetable -> Int 
fitness _ = 0

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

-- TODO: generate some timetables that respect the requirements
generateInitialEnts :: Int -> Requirements -> [SchoolTimetable]
generateInitialEnts _ _ = []