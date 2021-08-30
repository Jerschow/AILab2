# Firstorderlogicsolver
Converts BNF to CNF and then uses DPLL to satisfy the clause or find if the clause is not satisfiable.
How to run:
python3 main.py filename.txt
where filename.txt is where the sentences to be solved are written.
The following flags may also be included:
-convert: signifying that filename.txt is BNF to first be converted to CNF
-noconvert: signfiying that filename.txt is CNF that does not need to be converted
