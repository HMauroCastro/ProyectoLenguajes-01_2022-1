# ProyectoLenguajes-01_2022-1

# Ejemplo
### # es igual a Lambda

### SI es LL(1)
- reglas = E -> E + T | T,
         T -> T * F | F,
         F -> id | ( E )

- noTerminales = E, T, F
- terminales = id, +, *, (, )


### SI es LL(1)
- reglas = S -> A k f,
         A -> A d | a B | a C,
         C -> c,
         B -> b B C | r

- noTerminales = A, B, C
- terminales = k, f, d, a, c, b, r


### NO es LL(1)
- reglas = S -> A B C | C,
         A -> a | b B | #,
         B -> p | #,
         C -> c

- noTerminales = A, S, B, C
- terminales = a, c, b, p
