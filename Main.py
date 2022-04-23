import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk

"""---------------------------Diseño interfaz del proyecto-----------------------------------------------"""

# Se crea la ventana:
ventana = Tk()

# Se le da un tamaño:
ventana.geometry("1350x670")

# Agregando un titulo a la ventana
ventana.title("Proyecto Lenguajes")

# En este canvas colocaremos las herramientas que nos permitan manipular el programa
canvas_principal = Canvas(ventana, width=1350, height=670, bg="#2E065E")
canvas_principal.place(x=0, y=0)

"""--------------------------------------- Menú -----------------------------------------"""

# Insertar las reglas
lblReglas = Label(canvas_principal, fg="white", bg="#2E065E", width=18, text="Reglas",
                  font=("Comic Sans MS", 13)).place(x=75, y=20)

textReglas = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=25, height=5, font=("Comic Sans MS", 13))
textReglas.grid(column=0, row=2, padx=40, pady=60)
textReglas.focus()

# Insertar los no terminales
lblNoTerminales = Label(canvas_principal, fg="white", bg="#2E065E", width=18, text="No Terminales",
                        font=("Comic Sans MS", 11)).place(x=90, y=200)
txtNoTerminales = StringVar()
textNoTerminales = Entry(canvas_principal, width=30, textvariable=txtNoTerminales, font=("Comic Sans MS", 11)).place(
    x=40, y=230)

# Insertar los terminales
lblTerminales = Label(canvas_principal, fg="white", bg="#2E065E", width=18, text="Terminales",
                      font=("Comic Sans MS", 11)).place(x=90, y=280)
txtTerminales = StringVar()
textTerminales = Entry(canvas_principal, width=30, textvariable=txtTerminales, font=("Comic Sans MS", 11)).place(x=40,
                                                                                                                 y=310)

# Muestra información de Reglas
lstReglas = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=9, font=("Comic Sans MS", 11),
                    highlightbackground="white")
lstReglas.place(x=35, y=440)

# Muestra información de la Recursion
lstRecursion = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=14, font=("Comic Sans MS", 11),
                       highlightbackground="white")
lstRecursion.place(x=380, y=20)

# Muestra información de la factorizacion
lstFactorizacion = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=14, font=("Comic Sans MS", 11),
                           highlightbackground="white")
lstFactorizacion.place(x=700, y=20)

# Muestra información de Primeros
lstPrimeros = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=14, font=("Comic Sans MS", 11),
                      highlightbackground="white")
lstPrimeros.place(x=1020, y=20)

# Muestra información de Siguientes
lstSiguientes = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=14, font=("Comic Sans MS", 11),
                        highlightbackground="white")
lstSiguientes.place(x=380, y=350)

# Muestra información de Conjunto Prediccion
lstConjuntoPrediccion = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=14,
                                font=("Comic Sans MS", 11),
                                highlightbackground="white")
lstConjuntoPrediccion.place(x=700, y=350)

# Muestra información Si es una gramática LL(1)
lstEsGramaticaLL1 = Listbox(canvas_principal, fg="white", bg="#2E065E", width=33, height=5,
                            font=("Comic Sans MS", 11),
                            highlightbackground="white")
lstEsGramaticaLL1.place(x=1020, y=440)

"""--------------------------------------------------------------------------------------------"""


# Método para eliminar la recursión izquierda de las reglas, recibe el dic. de reglas y lo retorna limpio
def eliminarRecursionIzquierda(dicReglasALimpiar):
    dicReglasNuevas = {}

    for regla in dicReglasALimpiar:
        reglasConRecursion = []
        reglasSinRecursion = []
        totalReglas = dicReglasALimpiar[regla]

        for recursion in totalReglas:
            if recursion[0] == regla:
                reglasConRecursion.append(recursion[1:])
            else:
                reglasSinRecursion.append(recursion)

        if len(reglasConRecursion) != 0:
            # Agregar comilla (') a la nueva regla
            nuevaRegla = regla + "'"
            while (nuevaRegla in dicReglasALimpiar.keys()) \
                    or (nuevaRegla in dicReglasNuevas.keys()):
                nuevaRegla += "'"

            # Agregar regla sin Recursion
            for b in range(0, len(reglasSinRecursion)):
                reglasSinRecursion[b].append(nuevaRegla)
            dicReglasALimpiar[regla] = reglasSinRecursion

            # Agregar regla con recursion
            for a in range(0, len(reglasConRecursion)):
                reglasConRecursion[a].append(nuevaRegla)
            reglasConRecursion.append(['#'])
            # Adicionar Lambda
            dicReglasNuevas[nuevaRegla] = reglasConRecursion

    # Adicionar las nuevas reglas y retornar Reglas limpias
    for izquierda in dicReglasNuevas:
        dicReglasALimpiar[izquierda] = dicReglasNuevas[izquierda]
    return dicReglasALimpiar


# Método para eliminar la factotización izquierda de las reglas, recibe el dic. de reglas y lo retorna limpio
def eliminarFactorizacionIzquierda(dicReglasALimpiar):
    dicReglasNuevas = {}

    for regla in dicReglasALimpiar:
        totalReglas = dicReglasALimpiar[regla]
        dicTemporal = dict()
        for factorizacion in totalReglas:
            if factorizacion[0] not in list(dicTemporal.keys()):
                dicTemporal[factorizacion[0]] = [factorizacion]
            else:
                dicTemporal[factorizacion[0]].append(factorizacion)

        dicReglasExpandidasFactorizacion = []
        dicReglasConFactorizacion = {}

        for terminoIzquierda in dicTemporal:
            # Obtener el valor desde dicTemporal para terminoIzquierda
            empiezanConTermino = dicTemporal[terminoIzquierda]
            if len(empiezanConTermino) > 1:
                nuevaRegla = regla + "'"

                while (nuevaRegla in dicReglasALimpiar.keys()) \
                        or (nuevaRegla in dicReglasConFactorizacion.keys()):
                    nuevaRegla += "'"

                # Adicionar la nueva regla
                dicReglasExpandidasFactorizacion.append([terminoIzquierda, nuevaRegla])
                reglaExpandida = []
                for g in dicTemporal[terminoIzquierda]:
                    reglaExpandida.append(g[1:])
                dicReglasConFactorizacion[nuevaRegla] = reglaExpandida
            else:
                # Adicionar las que no requieren factorizacion
                dicReglasExpandidasFactorizacion.append(empiezanConTermino[0])

        # Agregar la regla original
        dicReglasNuevas[regla] = dicReglasExpandidasFactorizacion

        # Adicionar las nuevas reglas y retornar Reglas limpias
        for regla in dicReglasConFactorizacion:
            dicReglasNuevas[regla] = dicReglasConFactorizacion[regla]
    return dicReglasNuevas


# Método para calcular los primeros por cada regla, retorna el dic. con los resultados
def calcularPrimeros(regla):
    global reglas, noTerminales, \
        terminales, dicReglasLimpias, dicPrimeros

    # Para terminales o lambda
    if len(regla) != 0 and (regla is not None):
        if regla[0] in terminales:
            return regla[0]
        elif regla[0] == '#':
            return '#'

    # Condicion para no terminales
    if len(regla) != 0:
        if regla[0] in list(dicReglasLimpias.keys()):
            dicResultados = []
            reglasRecursion = dicReglasLimpias[regla[0]]

            for recursion in reglasRecursion:
                reglaIndividual = calcularPrimeros(recursion)
                if type(reglaIndividual) is list:
                    for i in reglaIndividual:
                        dicResultados.append(i)
                else:
                    dicResultados.append(reglaIndividual)

            if '#' not in dicResultados:
                return dicResultados
            else:
                nuevaLista = []
                dicResultados.remove('#')
                if len(regla) > 1:
                    nuevo = calcularPrimeros(regla[1:])
                    if nuevo != None:
                        if type(nuevo) is list:
                            nuevaLista = dicResultados + nuevo
                        else:
                            nuevaLista = dicResultados + [nuevo]
                    else:
                        nuevaLista = dicResultados
                    return nuevaLista

                dicResultados.append('#')
                return dicResultados


# Método para calcular los siguientes por cada regla, retorna el dic. con los resultados
def calcularSiguientes(regla):
    global simboloInicial, reglas, noTerminales, \
        terminales, dicReglasLimpias, dicPrimeros, dicSiguientes

    # Simbolo de inicio $
    resultadoSiguiente = set()
    if regla == simboloInicial:
        resultadoSiguiente.add('$')

    # Verificar todas las reglas
    for reglaNT in dicReglasLimpias:
        rhs = dicReglasLimpias[reglaNT]

        for reglaSeparada in rhs:
            if regla in reglaSeparada:
                while regla in reglaSeparada:
                    nombreNoTerminal = reglaSeparada.index(regla)
                    reglaSeparada = reglaSeparada[nombreNoTerminal + 1:]

                    if len(reglaSeparada) != 0:
                        resultado = calcularPrimeros(reglaSeparada)

                        if '#' in resultado:
                            nuevaLista = []
                            resultado.remove('#')
                            nuevo = calcularSiguientes(reglaNT)
                            if nuevo != None:
                                if type(nuevo) is list:
                                    nuevaLista = resultado + nuevo
                                else:
                                    nuevaLista = resultado + [nuevo]
                            else:
                                nuevaLista = resultado
                            resultado = nuevaLista
                    else:
                        if regla != reglaNT:
                            resultado = calcularSiguientes(reglaNT)

                    # Adicionar resultados de calcularSiguiente
                    if resultado is not None:
                        if type(resultado) is list:
                            for g in resultado:
                                resultadoSiguiente.add(g)
                        else:
                            resultadoSiguiente.add(resultado)
    return list(resultadoSiguiente)


# Método que hace el proceso de mostrar los primeros, se llama el método de recursión y factorización
def mostrarPrimeros():
    global reglas, noTerminales, \
        terminales, dicReglasLimpias, dicPrimeros

    lstPrimeros.delete(0, END)
    lstPrimeros.insert(END, "\n-------- PRIMEROS --------", "")

    for regla in reglas:
        r = regla.split("->")

        # Elimnar espacios en blanco
        r[0] = r[0].strip()
        r[1] = r[1].strip()
        reglaTotal = r[1]

        reglaSeparada = reglaTotal.split('|')

        for i in range(len(reglaSeparada)):
            reglaSeparada[i] = reglaSeparada[i].strip()
            reglaSeparada[i] = reglaSeparada[i].split()
        dicReglasLimpias[r[0]] = reglaSeparada

    lstReglas.delete(0, END)
    lstReglas.insert(END, f"\n-------- REGLAS LEÍDAS --------", "")
    for nombreRegla in dicReglasLimpias:
        lstReglas.insert(END, f"{nombreRegla} -> {dicReglasLimpias[nombreRegla]}")

    lstRecursion.delete(0, END)
    lstRecursion.insert(END, f"\n---- ELIM. RECURSIÓN IZQUIERDA ----", "")
    dicReglasLimpias = eliminarRecursionIzquierda(dicReglasLimpias)

    for nombreRegla in dicReglasLimpias:
        lstRecursion.insert(END, f"{nombreRegla} -> {dicReglasLimpias[nombreRegla]}")

    lstFactorizacion.delete(0, END)
    lstFactorizacion.insert(END, "\n-- ELIM. FACTORIZACIÓN IZQUIERDA --", "")
    dicReglasLimpias = eliminarFactorizacionIzquierda(dicReglasLimpias)

    for nombreRegla in dicReglasLimpias:
        lstFactorizacion.insert(END, f"{nombreRegla} -> {dicReglasLimpias[nombreRegla]}")

    # Calcular conjunto primeros por cada regla
    for nombreRegla in list(dicReglasLimpias.keys()):
        conjuntoPrimeros = set()
        for sub in dicReglasLimpias.get(nombreRegla):
            resultadoPrimeros = calcularPrimeros(sub)
            if resultadoPrimeros != None:
                if type(resultadoPrimeros) is list:
                    for u in resultadoPrimeros:
                        conjuntoPrimeros.add(u)
                else:
                    conjuntoPrimeros.add(resultadoPrimeros)

        dicPrimeros[nombreRegla] = conjuntoPrimeros
        lstPrimeros.insert(END, f"Primeros({nombreRegla}) " f"=> {conjuntoPrimeros}")


# Método que hace el proceso de mostrar los siguientes
def mostrarSiguientes():
    global simboloInicial, reglas, noTerminales, \
        terminales, dicReglasLimpias, dicPrimeros, dicSiguientes

    lstSiguientes.delete(0, END)
    lstSiguientes.insert(END, "\n-------- SIGUIENTES --------", "")

    for nombreRegla in dicReglasLimpias:
        conjuntoSiguientes = set()
        resultado = calcularSiguientes(nombreRegla)
        if resultado is not None:
            for g in resultado:
                conjuntoSiguientes.add(g)
        dicSiguientes[nombreRegla] = conjuntoSiguientes
        lstSiguientes.insert(END, f"Siguientes({nombreRegla})" f" => {conjuntoSiguientes}")


# Método que hace el proceso para mostrar el conjunto predicción
def mostrarConjuntoPrediccion():
    import copy
    global dicReglasLimpias, dicPrimeros, dicSiguientes, terminales

    # Crear matriz de filas(NT) x [columnas(T) + 1($)]
    # Crear lista de no terminales
    listaNoTerminales = list(dicReglasLimpias.keys())
    copiaTerminales = copy.deepcopy(terminales)
    copiaTerminales.append('$')

    # Crear la matriz
    matriz = []
    for x in dicReglasLimpias:
        filas = []
        for produccionDeNT in copiaTerminales:
            filas.append('')
        matriz.append(filas)

    # Clasificar la gramática si es LL(1) o no es LL(1)
    esGramaticaLL1 = True

    # Limpiar Caja Conjunto Predicción
    lstConjuntoPrediccion.delete(0, END)
    lstConjuntoPrediccion.insert(END, "\n---- CONJUNTO PREDICCIÓN ----", "")

    for nombreNoTerminal in dicReglasLimpias:
        rhs = dicReglasLimpias[nombreNoTerminal]
        for produccionDeNT in rhs:
            resultadoConjuntoProduccion = calcularPrimeros(produccionDeNT)

            if '#' in resultadoConjuntoProduccion:
                if type(resultadoConjuntoProduccion) == str:
                    siguientePrimero = []
                    siguienteOp = dicSiguientes[nombreNoTerminal]
                    if siguienteOp is str:
                        siguientePrimero.append(siguienteOp)
                    else:
                        for u in siguienteOp:
                            siguientePrimero.append(u)
                    resultadoConjuntoProduccion = siguientePrimero
                else:
                    resultadoConjuntoProduccion.remove('#')
                    resultadoConjuntoProduccion = list(resultadoConjuntoProduccion) + \
                                  list(dicSiguientes[nombreNoTerminal])

            # Agregar reglas a la tabla
            tablaTemporal = []
            if type(resultadoConjuntoProduccion) is str:
                tablaTemporal.append(resultadoConjuntoProduccion)
                resultadoConjuntoProduccion = copy.deepcopy(tablaTemporal)
            for c in resultadoConjuntoProduccion:
                xNoTerminal = listaNoTerminales.index(nombreNoTerminal)
                yTerminal = copiaTerminales.index(c)
                if matriz[xNoTerminal][yTerminal] == '':
                    matriz[xNoTerminal][yTerminal] = matriz[xNoTerminal][yTerminal] \
                                   + f"{nombreNoTerminal}->{' '.join(produccionDeNT)}"

                else:

                    # Si la regla ya esta presente
                    if f"{nombreNoTerminal}->{produccionDeNT}" in matriz[xNoTerminal][yTerminal]:
                        continue
                    else:
                        esGramaticaLL1 = False
                        matriz[xNoTerminal][yTerminal] = matriz[xNoTerminal][yTerminal] \
                                       + f",{nombreNoTerminal}->{' '.join(produccionDeNT)}"
            lstConjuntoPrediccion.insert(END, f"CP({nombreNoTerminal} -> {''.join(produccionDeNT)}) => {set(resultadoConjuntoProduccion)}")

    if esGramaticaLL1 == True:
        lstEsGramaticaLL1.delete(0, END)
        lstEsGramaticaLL1.insert(END, "", "", "\n       **  SI es una Gramática LL(1)  **")
    if esGramaticaLL1 == False:
        lstEsGramaticaLL1.delete(0, END)
        lstEsGramaticaLL1.insert(END, "", "", "\n       **  NO es una Gramática LL(1)  **")


# Método para quitar los espacios de una palabra, ayuda en los terminales y no terminales
def quitarEspacios(palabra):
    salida = []
    for i in palabra:
        salida.append(i.strip())
    return salida


# Iniciar el Programa, lo activa el boton "iniciar"
def iniciarPrograma():
    global simboloInicial, reglas, noTerminales, terminales, dicReglasLimpias, dicPrimeros, dicSiguientes

    if txtTerminales.get() == "" or txtNoTerminales.get() == "":
        messagebox.showerror(message="Falta llenar algún campo", title="Error")
    else:
        reglas = textReglas.get(1.0, END).split(',')
        terminales = quitarEspacios(txtTerminales.get().split(','))
        noTerminales = quitarEspacios(txtNoTerminales.get().split(','))
        simboloInicial = noTerminales[0]
        dicReglasLimpias = {}
        dicPrimeros = {}
        dicSiguientes = {}
        mostrarPrimeros()
        mostrarSiguientes()
        mostrarConjuntoPrediccion()


'''---------------------------------------- Botonera -----------------------------------------'''

# Este botón inicia el programa:
btn_Iniciar = Button(canvas_principal, fg="white", bg="#1E6F4A", width=15, text="Iniciar", font=("Comic Sans MS", 10),
                     command=iniciarPrograma).place(x=30, y=370)

# Este botón termina el programa:
btn_Salir = Button(canvas_principal, fg="white", bg="#1E6F4A", width=15, text="Salir", font=("Comic Sans MS", 10),
                   command=sys.exit).place(x=190, y=370)

ventana.mainloop()
