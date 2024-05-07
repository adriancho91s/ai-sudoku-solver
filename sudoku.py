'''
Integrantes:  - Juan David García Arce
              - Adrian Fernando Gaitán
              - Maximiliano Giraldo Ocampo

Tipo de busqueda: Deep first search.
'''

#_________________________LIBRERÍAS_________________________#
import copy
import itertools
from colorama import Fore, Style

import tkinter as tk

def visualize_sudoku(sudoku):
    colsIndex = "ABCDEFGHI"  # Columnas
    root = tk.Tk()
    root.title("Sudoku Resuelto")

    # Title
    title_label = tk.Label(root, text="Sudoku Resuelto", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=10, pady=(10, 5))

    # Sudoku grid
    for i in range(9):
        for j in range(9):
            cell_value = sudoku.Vars[colsIndex[j] + str(i + 1)].pop()
            sudoku.Vars[colsIndex[j] + str(i + 1)].add(cell_value)

            # Add thicker lines to mark regions
            border_width = 1
            if i % 3 == 0 and i != 0:
                border_width = 2
            if j % 3 == 0 and j != 0:
                border_width = 2

            label = tk.Label(root, text=str(cell_value), width=4, height=2, relief="solid", font=("Arial", 16),
                             borderwidth=border_width)
            label.grid(row=i + 2, column=j + 1, padx=1, pady=1)

    # Region labels
    for i in range(9):
        label = tk.Label(root, text=colsIndex[i], width=4, height=2, font=("Arial", 10))
        label.grid(row=1, column=i + 1, padx=1, pady=1)
        label = tk.Label(root, text=str(i + 1), width=4, height=2, font=("Arial", 10))
        label.grid(row=i + 2, column=0, padx=1, pady=1)

    # Author's details
    team_details = [
        "Authors:",
        "   - Adrian Fernando Gaitán",
        "   - Juan David García Arce",
        "   - Maximiliano Giraldo Ocampo"
    ]

    # Display author's details
    for index, detail in enumerate(team_details):
        team_info_label = tk.Label(root, text=detail, font=("Arial", 12))
        team_info_label.grid(row=12 + index, column=0, columnspan=10, sticky='w')

    root.mainloop()

#_________________________ESTRUCTURA CSP_________________________#
class CSP:
    def __init__(self):
        self.Vars = {}  # Variables.
        self.Constraints={'Dif':[], 'SameDomain2': [], 'SameDomain3': [], 'NotRepeated': []}  # Restricciones.
        self.checkReductions = False # Booleano de verificación de reducciones.
        self.counterLoop = 0 # Limite de pruebas con depth first search

    '''DOMINIOS DE LAS VARIABLES'''

    '''
    Estructura de los dominios de las variables:

            +---+---+---+---+---+---+---+---+---+---+
    Sudoku: | / | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | A | *   *   * | *   *   * | *   *   * |
            | B | *   *   * | *   *   * | *   *   * |
            | C | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | D | *   *   * | *   *   * | *   *   * |
            | E | *   *   * | *   *   * | *   *   * |
            | F | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | G | *   *   * | *   *   * | *   *   * |
            | H | *   *   * | *   *   * | *   *   * |
            | I | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+

            Genera la estructura de los dominios de variables para el tablero de Sudoku.

    '''

    def Vars_Doms(self):
        rows = set(range(1, 10))
        cols = 'ABCDEFGHI'
        self.Vars = {f"{c}{r}": rows.copy() for c in cols for r in rows}

    """
    Establece un valor específico en el diccionario de variables.

    Args:
        Name (str): El nombre de la variable para establecer el valor.
        Value (int): El valor a establecer para la variable.

    Returns:
        None
    """


    def setValueInVars(self,Name,Value):
        self.Vars[Name] = {Value}

    """
    Inicializa el tablero de Sudoku leyendo valores de un archivo y asignándolos a variables.

    Args:
        nameFile (str): El nombre del archivo que contiene los valores del tablero de Sudoku.

    Returns:
        None
    """

    def initBoard(self, nameFile):
        with open(nameFile, "r") as file:
            ListSudoku = "ABCDEFGHI"
            for r, c in itertools.product(range(1, 10), ListSudoku):
                cur = int(file.readline())
                if cur < 10:
                    self.setValueInVars(f"{c}{r}", cur)

    '''   RESTRICCIONES DE LAS VARIABLES

        - Itera sobre el rango de números de fila y columnas, creando una lista de variables para cada fila y añadiéndola al diccionario de restricciones bajo la clave dada.
    '''

    # Restricciones de las filas.
    def rowConstraints(self, consKey):
        colsIndex = "ABCDEFGHI"
        for i in range(1, 10):
            restrictionList = [str(j) + str(i) for j in colsIndex]
            self.Constraints[consKey].append(restrictionList)

    # Restricciones de las columnas.
    def colConstraints(self, consKey):
        colsIndex = "ABCDEFGHI"
        for i in colsIndex:
            restrictionList = [str(i) + str(j) for j in range(1, 10)]
            self.Constraints[consKey].append(restrictionList)

    # Restricciones de las ventanas.
    def regionConstraints(self, consKey, startRange, endRange):
        triplets = ["ABC", "DEF", "GHI"]
        for t in triplets:
            restrictionList = []
            for c in t:
                restrictionList.extend(str(c) + str(i) for i in range(startRange, endRange))
            self.Constraints[consKey].append(restrictionList)

    # Estructura de las restricciones.
    def constraintStructures(self, consKey):
        self.Constraints[consKey] = [] # Se inicializa la restricción.
        self.rowConstraints(consKey)
        self.colConstraints(consKey)
        startRange = [1, 4, 7]
        endRange = [4, 7, 10]
        for index in range(3):
            self.regionConstraints(consKey, int(startRange[index]), int(endRange[index]))

    '''
    Restricciones de diferencias:

      - Si el dominio de la variable es 1, se elimina el elemento de las demás variables.

      - Si el dominio es 2, se eliminan los elementos de las demás variables si los dominios son iguales.

      - Si el dominio es 3, se eliminan los elementos de las demás variables si los dominios son iguales.
    '''
    def dif(self, list_, index):
        for var in list_:
            if (self.numElement(var) == 1):
                element = self.Vars[var] 
                self.deleteElementInVar(var, list_, element.copy())
                self.deleteVarInConstraint('Dif', var, index)

    # Restricciones de dominios iguales de 2.
    def SameDomain2(self):
        for constraint in self.Constraints['SameDomain2']:
            for var_1 in constraint:
                if (self.numElement(var_1) == 2):
                    for var_2 in constraint:
                        if var_1 != var_2 and self.Vars[var_1] == self.Vars[var_2]:
                            lista_valores = list(self.Vars[var_1])
                            # Se obtienen los valores del dominio.
                            val_1 = lista_valores[0]
                            val_2 = lista_valores[1]
                            for valForDelete in constraint:
                                if valForDelete not in [var_1, var_2]:
                                    lenBefore = len(self.Vars[valForDelete])
                                    # Se eliminan los elementos del dominio.
                                    self.Vars[valForDelete].discard(val_1)
                                    self.Vars[valForDelete].discard(val_2)
                                    lenAfter = len(self.Vars[valForDelete])
                                    if(lenBefore > lenAfter):
                                        self.checkReductions = True

    # Restricciones de dominios iguales de 3.
    def SameDomain3(self):
        for constraint in self.Constraints['SameDomain3']:
            for var_1 in constraint:
                if self.numElement(var_1) == 3:
                    domain = self.Vars[var_1]
                    if all(self.Vars[var] == domain for var in constraint if var != var_1):
                        for varForDelete in constraint:
                            original_len = len(self.Vars[varForDelete])
                            self.Vars[varForDelete] -= domain
                            if len(self.Vars[varForDelete]) < original_len:
                                self.checkReductions = True


    # Restricciones de no repetidos.
    def NotRepeated(self):
        for constraint in self.Constraints['NotRepeated']:
            all_values = set()
            for var in constraint:
                all_values.update(self.Vars[var])
            for value in all_values:
                count = 0
                for var in constraint:
                    if value in self.Vars[var]:
                        count += 1
                        var_unic = var
                if count == 1 and self.numElement(var_unic) != 1:
                    # Si el valor se encuentra en un solo dominio, se actualiza el dominio de la variable.
                    self.Vars[var_unic] = {value}
                    self.checkReductions = True

    """
    Elimina un elemento del dominio de una variable en una lista dada, excepto la variable especificada.

    Args:
        var: La variable de la que se elimina el elemento.
        list_: La lista de variables para actualizar el dominio.
        element: El elemento a eliminar del dominio de las variables.

    Returns:
        None
    """
    def deleteElementInVar(self, var, list_, element):
        integer_element = int(element.pop())
        for c in list_:
            if c != var:
                self.Vars[c].discard(integer_element)
                self.checkReductions = True

    # Se elimina la variable de la restricción.
    def deleteVarInConstraint(self, constKey, var, i):
        lista = self.Constraints[constKey][i]
        lista.remove(var)

    """
    Devuelve la longitud del dominio de una variable.

    Args:
        key: La clave de la variable para determinar la longitud del dominio.

    Returns:
        int: La longitud del dominio de la variable.
    """
    def numElement(self, key):
        return len(self.Vars[key])

    """
    Detect break memory
    """
    def detectBreak(self):
        if (self.counterLoop == 12):
            print("No se pudo resolver")
            return True

    """
    Procesa las restricciones para verificar la consistencia y aplicar operaciones específicas.

    Returns:
        bool: True si se realizaron reducciones durante el procesamiento de las restricciones, False en caso contrario.
    """
    def loopThroughConstraint(self):
        self.checkReductions = False
        for index in range(len(self.Constraints['Dif'])):
            self.dif(self.Constraints['Dif'][index], index)
            # Se verifica si el sudoku es consistente.
        self.SameDomain2()
        self.SameDomain3()
        self.NotRepeated()
        return self.checkReductions

    # Se verifica si el sudoku está resuelto.
    def is_solved(self):
        colsIndex = "ABCDEFGHI" # Columnas.
        return all(
            len(self.Vars[str(c) + str(i)]) == 1
            for c, i in itertools.product(colsIndex, range(1, 10))
        )

    # Se verifica si el sudoku es consistente.
    def localConsistent(self):
        colsIndex = "ABCDEFGHI"
        return all(
            len(self.Vars[str(c) + str(i)]) != 0
            for c, i in itertools.product(colsIndex, range(1, 10))
        )

    # Se copia el objeto.
    def copy(self):
        return copy.deepcopy(self)

    """
    Realiza el backtracking para resolver el rompecabezas de Sudoku.

    Args:
        sudoku: El rompecabezas de Sudoku a resolver.

    Returns:
        bool: True si se resuelve el rompecabezas, False en caso contrario.
    """
    def backTracking(self, sudoku):
        colsIndex = "ABCDEFGHI"
        break_outer_loop = False # Variable que nos indica si se realizó alguna eliminación en el dominio de las variables.
        for c in colsIndex:
            for i in range(1,10):
                print(f"Variable: {c}{i}")
                if (len(self.Vars[str(c) + str(i)]) == 2):
                    lista = list(self.Vars[str(c) + str(i)])
                    element = lista[0]
                    self.Vars[str(c) + str(i)].discard(element)
                    break_outer_loop = True
                    break
            if break_outer_loop: # Se verifica si se realizó alguna eliminación en el dominio de las variables. 
                break
        if(c == "I" and i == 9):
            self.counterLoop += 1
        if(break_outer_loop): # Se verifica si se realizó alguna eliminación en el dominio de las variables.
            while(self.loopThroughConstraint()):
               pass
            if (self.localConsistent() == False):
                sudoku.Vars[str(c) + str(i)] = {element} # Se actualiza la variable.
                return False
            else:
                return True
        else:
            return("No tiene solucion")


def print_sudoku(sudoku):
    colsIndex = "ABCDEFGHI" # Columnas
    numbers_color = Fore.GREEN
    letters_color = Fore.BLUE
    region_color = Fore.RED

    print("SUDOKU RESUELTO: ")
    print("\t" + region_color + "+---" * 10 + "+" + Style.RESET_ALL)
    print("\t| / | " + letters_color + "A" + Style.RESET_ALL + " | " + letters_color + "B" + Style.RESET_ALL + " | " + letters_color + "C" + Style.RESET_ALL + " | " + letters_color + "D" + Style.RESET_ALL + " | " + letters_color + "E" + Style.RESET_ALL + " | " + letters_color + "F" + Style.RESET_ALL + " | " + letters_color + "G" + Style.RESET_ALL + " | " + letters_color + "H" + Style.RESET_ALL + " | " + letters_color + "I" + Style.RESET_ALL + " |")
    print("\t" + region_color + "+---" * 10 + "+" + Style.RESET_ALL)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("\t" + region_color + "+---" * 10 + "+" + Style.RESET_ALL)
        row_values = []
        for j in range(9):
            cell_value = sudoku.Vars[colsIndex[j] + str(i+1)].pop()
            row_values.append(str(cell_value))
            sudoku.Vars[colsIndex[j] + str(i+1)].add(cell_value)
        print("\t| " + numbers_color + str(i+1) + Style.RESET_ALL + " | " + " | ".join(row_values) + " |")
    print("\t" + region_color + "+---" * 10 + "+" + Style.RESET_ALL)


#_________________________SUDOKU_________________________#
sudoku = CSP() # Se crea el objeto CSP.
sudoku.Vars_Doms()
sudoku.initBoard("board") # Se inicializa el tablero de Sudoku.
sudoku.constraintStructures('Dif')
sudoku.constraintStructures('SameDomain2')
sudoku.constraintStructures('SameDomain3')
sudoku.constraintStructures('NotRepeated')

# Se resuelve el sudoku.
while(sudoku.is_solved() == False):
    breakMemory = sudoku.detectBreak() #Detect memory break
    while(sudoku.loopThroughConstraint()):
        if (breakMemory):
            break
        pass
    if (breakMemory):
        break
    if sudoku.is_solved() == False:
        test = sudoku.copy() # Se copia el objeto.
        if test.backTracking(sudoku) != False:
            sudoku = test # Se actualiza el sudoku.

#_________________________IMPRESIÓN DEL SUDOKU_________________________#
if (not(breakMemory)):
    print_sudoku(sudoku)
    visualize_sudoku(sudoku)
#_________________________FIN DEL PROGRAMA_________________________#