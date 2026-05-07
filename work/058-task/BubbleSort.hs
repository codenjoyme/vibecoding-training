module BubbleSort where

bubbleSort :: Ord a => [a] -> [a]
bubbleSort xs
    | xs == bubbled = xs
    | otherwise     = bubbleSort bubbled
  where
    bubbled = bubble xs

bubble :: Ord a => [a] -> [a]
bubble []       = []
bubble [x]      = [x]
bubble (x:y:rest)
    | x > y     = y : bubble (x : rest)
    | otherwise = x : bubble (y : rest)

main :: IO ()
main = do
    let xs = [64, 34, 25, 12, 22, 11, 90] :: [Int]
    putStrLn $ "Before: " ++ show xs
    putStrLn $ "After:  " ++ show (bubbleSort xs)
