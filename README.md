#AccPred

## Trial Splitting
- restrict the appearance of each type of sentence to **once** in the whole experiment
### Steps:
1. Assign Relatedness:
    - Shuffle, split list in 2
    - 1st Half: Rel, 2nd Half: Unrel
    - Store subsets *might wanna change this maybe to reduce storage steps*?
2. Assign Speaker:
    - For each subsets of Relatedness assigned lists:
        - shuffle, split in 2
        - First half: Native, 2nd Half: Non-Natuve
    - Store subsets
3. Join Lists:
    - Concatenate all sublists created from step 2
    - Re-shuffle for good measure.
4. From this global file, re-create the file name as a **UNIQUE ID**.
5. Merge this table with the file containing all other measures and variables?
    *This step is a maybe... After all if I have the info, I can always go back and find the variables like cloze ratings etc from the index files post-hoc, rather that making the programme always carry it.**
    -> Probably better to stick to only the experimentally needed info in that trial list.
