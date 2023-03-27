import time
import os
import csv

preguntas = ["ID del empleado: ", "Nombre del Empleado: ", "Edad del empleado: ", "Peso en Kg del empleado: ", "Estatura en metros del empleado: ", "Tiene diabetes(0: no | 1: si): ", "Tiene hipertensión(0: no | 1: si): ", "Tiene problemas de corazon(0: no | 1: si): ", "Tiene cancer(0: no | 1: si): ", "Tiene tabaquismo(0: no | 1: si): ", "Está Vacunado(0: no | 1: si): ", "Número de departamento: "]
condiciones = ["diabetes", "hipertensión", "corazon", "cancer", "tabaquismo", "vacunado"]
clasificaciones = ["Delgadez severa", "Delgadez moderada", "Delgadez aceptable", "Peso Normal", "Sobrepeso"]
empleados = []
condiciones_frec = []
empleados_depto = []

# Funcion para leer los datos de el archivo empleados.csv
def leer_archivo(nombre_archivo):
    if os.path.isfile('./' + str(nombre_archivo)):
        with open(nombre_archivo, newline="") as archivo_csv:
            lector = csv.reader(archivo_csv)

            # hay que tomar en cuenta que todos los elementos de la lista son str, por eso debemos convertirlos segun sea necesario
            for renglon in lector:
                renglon[2] = int(renglon[2])
                try:
                    renglon[3] = int(renglon[3])
                except ValueError:
                    renglon[3] = float(renglon[3])
                try:
                    renglon[4] = int(renglon[4])
                except ValueError:
                    renglon[4] = float(renglon[4])
                empleados.append(renglon)
    else:
        f = open(nombre_archivo, "w", newline="")
        f.close()


def grabar_archivo(nombre, lista):
    # Accesar el archivo con los argumentos ingresados a la funcion
    with open(nombre, 'w', newline='') as archivo:
        write = csv.writer(archivo)
        write.writerows(lista)


def verificar_depto(depto):
    for empleado in empleados:
        if depto == empleado[11]:
            empleados_depto.append(empleado)
    if empleados_depto == []:
        return False
    else:
        return True


def verificar_id(ID):
    for empleado in empleados:
        if empleado == []:
            return [False, None]
        elif ID == empleado[0]:
            return [True, empleados.index(empleado)]
    return [False, None]


def alta_empleado(archivo):
    leer_archivo(archivo)
    os.system('cls')
    empleados.append([])
    puntero = 0
    while puntero < len(preguntas):
        dato = input(preguntas[puntero])
        if puntero == 0:
            existe, indice = verificar_id(dato)
            if existe: 
                print(f"El ID que usted ingreso ({empleados[indice][0]}) ya existe. Intente de nuevo.")
                continue
        # Si el dato ingresado es un numero, dara un error y pedira que intente de nuevo.
        elif puntero > 0 and puntero < 2:
            if dato.isdigit():
                print(f'"{dato}" no es un nombre. Intente de nuevo')
                time.sleep(2)
                continue
        elif puntero < 5 and puntero > 1:
            try:
                dato = int(dato)
            except ValueError:
                try:
                    dato = float(dato)
                except ValueError:
                    print("Este valor deberá ser numérico. Intente de nuevo")
                    time.sleep(2)
                    continue
        elif puntero > 4 and puntero < 11:
            if dato not in ["1", "0"]:
                print("Este dato debera ser 1 (si) o 0 (no). intente de nuevo")
                time.sleep(2)
                continue
        empleados[len(empleados) - 1].append(dato)
        puntero += 1
    grabar_archivo(archivo, empleados)
    os.system('cls')
    print("El empleado se ha guardado con éxito!\n")
    print(", ".join([str(elem) for elem in empleados[len(empleados) - 1]]), "\n")
    empleados.clear()
    time.sleep(3)
    os.system('cls')

def calcular_imc_empleado(archivo):
    leer_archivo(archivo)
    os.system('cls')
    clasificacion_frec = []
    clasificacion_n = [0] * 5
    lista_diag = []
    lista_imc = []
    # Iteramos por cada empleado en la lista de empleados y calculamos su imc
    for empleado in empleados:
        imc = round(empleado[3] / empleado[4] ** 2, 2)
        lista_imc.append(imc)
        # Verificar que clasificacion asignarle a dicho empleado
        # Tambien agregamos la clasificacion a la lista de lista_diag que se encargara de almacenar estos datos para despues ser desplegados.
        if imc < 16:
            clasificacion_n[0] += 1
            lista_diag.append(clasificaciones[0])
        elif imc < 17:
            clasificacion_n[1] += 1
            lista_diag.append(clasificaciones[1])
        elif imc < 18.5:
            clasificacion_n[2] += 1
            lista_diag.append(clasificaciones[2])
        elif imc < 25:
            clasificacion_n[3] += 1
            lista_diag.append(clasificaciones[3])
        else:
            clasificacion_n[4] += 1
            lista_diag.append(clasificaciones[4])

    lista_ordenada = list(zip(lista_diag, lista_imc, empleados))
    lista_ordenada.sort()

    print("{:<21} {:<7} {:<7} {:<25} {:<10} {:<10} {:<80} {:}".format("Clasificación de IMC", "IMC", "ID", "Nombre", "Peso", "Estatura", "Condiciones", "Vacuna"))
    for diag, imc, empleado in lista_ordenada:
        print("{:<21} {:<7}".format(diag, imc), end=" ")

        # Solo queremos mostrar el ID, peso, estatura y sus condiciones
        # Iteramos por cada elemento de la variable empleado, que es la sublista correspondiente al empleado, y imprimimos los datos correspondiente basando en el indice de dicha lista
        # Solo se imprimiran los indices 0, 1, 3 y 4 que corresponden al ID, Nombre, Peso y Altura respectivamente
        for elem in range(len(empleado) - 1):
            if elem == 0:
                print("{:<7}".format(empleado[elem]), end=" ")
            elif elem == 1:
                print("{:<25}".format(empleado[elem]), end=" ")
            elif elem == 3:
                print("{:<10}".format(empleado[elem]), end=" ")
            elif elem == 4:
                print("{:<10}".format(empleado[elem]), end=" ")
            elif elem > 4:
                if empleado[elem] == "1":
                    print("{:<15}".format(
                        condiciones[elem - 5]), end=" ")
                else:
                    print("{:<15}".format("____________"), end=" ")
        print()

    for cant in clasificacion_n:
        try:
            clasificacion_frec.append(round(cant / len(empleados) * 100, 2))
        except ZeroDivisionError:
            break

    print("{:<21} {:<13} {:<10}".format("Clasificación de IMC", "Cantidad", "Porcentaje"))
    for clasif, cant, frec in zip(clasificaciones, clasificacion_n, clasificacion_frec):
        print(f"{clasif:<21} {cant:^8} {frec:>10}%")
    print(f"\nTotal de empleados: {len(empleados)}\n")
    empleados.clear()

def cambiar_info_empleado(archivo):
    leer_archivo(archivo)
    os.system('cls')
    # Obtenemos el indice que corresponde a la sublista dentro de empleados.
    while True:
        # Pedimos el Id del empleado.
        ID = input("Ingrese el ID del empleado que desea modificar: ")
        existe, indice = verificar_id(ID)

        if existe:
            break
        else:
            print("El ID que ingreso no existe. Intente de nuevo")

    # Mostramos toda la info del empleado primero
    print(", ".join([str(elem) for elem in empleados[indice]]), "\n")
    copia_empleado = empleados[indice].copy()

    vcc = 1
    while vcc < len(preguntas):
        # Como la lista contiene diferentes tipos de dato, tenemos que verificar que el usuario ingrese lo adecuado.
        # Primero pedimos el dato. Lo que se mostrara sera la pregunta que corresponde al indice en la lista de preguntas. Esto no incluye el ID.
        dato = input(preguntas[vcc])
        # Si el usuario no ingresa nada, le sumara 1 a la vcc y se reiniciara el ciclo.
        if dato == "":
            vcc += 1
            continue
        if vcc > 0 and vcc < 2:
            # Verificamos que el dato no sea numerico
            if dato.isdigit():
                print(f'"{dato}" no es un nombre. Intente de nuevo')
                time.sleep(2)
                continue
        elif vcc < 5 and vcc > 1:
            # Verificamos que el dato sea numerico
            try:
                dato = int(dato)
            except ValueError:
                try:
                    dato = float(dato)
                except ValueError:
                    print("Este valor deberá ser numérico. Intente de nuevo")
                    time.sleep(2)
                    continue
        elif vcc > 4 and vcc < 11:
            # Verificamos que el dato corresponda con las opciones
            if dato not in ["1", "0"]:
                print("Este dato debera ser 1 (si) o 0 (no). intente de nuevo")
                time.sleep(2)
                continue
        
        empleados[indice][vcc] = dato
        vcc += 1

    # Hacemos la pregunta para verificar que si quiere cambiar los datos del empleado
    respuesta = input("¿Está seguro de que quiere actualizar los datos del empleado? (y/n): ")

    while True:
        if respuesta.lower() == "y":
            print("El empleado se ha guardado con éxito!\n")
            print(", ".join([str(elem) for elem in empleados[indice]]), "\n")
            break
        elif respuesta.lower() == "n":
            empleados[indice] = copia_empleado
            print("La información del empleado se ha restablecido.")
            print(", ".join([str(elem) for elem in empleados[indice]]), "\n")
            break
        else:
            print(f'"{respuesta}" no es una respuesta valida. Intente de nuevo.')

    # Llamara la funcion empleados y guardara el nuevo empleado en el archivo
    grabar_archivo(archivo, empleados)
    empleados.clear()
    time.sleep(3)
    os.system('cls')

def consultar_empleado(archivo):
    leer_archivo(archivo)
    os.system('cls')
    while True:
        ID = input("Ingrese el ID: ")
        existe, indice = verificar_id(ID)

        if existe:
            break
        else: 
            print("El ID que ingreso no existe. Intente de nuevo")

    # Imprimimos el nombre de cada columna usando. format()
    print("{:<8} {:<25} {:<10} {:<10} {:<10} {:<80} {:}".format("ID", "Nombre", "Edad", "Peso", "Estatura", "Condiciones", "Vacuna"))
    for elem in range(len(empleados[indice]) - 1):
        # Dependiendo del el indice, es la cantidad de espacios hacia a la izquierda que agregamos. Para esto usamos las siguientes condiciones.
        if elem == 0:
            print("{:<8}".format(empleados[indice][elem]), end=" ")
        elif elem == 1:
            print("{:<25}".format(empleados[indice][elem]), end=" ")
        elif elem < 5:
            print("{:<10}".format(empleados[indice][elem]), end=" ")
        # Si elem es mayor a 5 aplicaremos el mismo formato para las condiciones ("diabetes", "hipertensión","corazon", "cancer", "tabaquismo", "vacuna")
        else:
            # Si el dato es igual a uno agregamos la condicion correspondiente en la lista de condiciones, de lo contrario solo se pondra una linea.
            if empleados[indice][elem] == "1":
                print("{:<15}".format(condiciones[elem - 5]), end=" ")
            else:
                print("{:<15}".format("____________"), end=" ")
    print("\n")
    empleados.clear()

def reporte_empleados(empleados_lista, archivo):
    # Leer el archivo de empleados con el argumento archivo recibido por la funcion
    leer_archivo(archivo)
    condiciones_n = [0] * 6
    os.system('cls')
    # Imprimimos el nombre de cada columna.
    print("{:<8} {:<25} {:<10} {:<10} {:<10} {:<79} {:<0}".format("ID", "Nombre", "Edad", "Peso", "Estatura", "Condiciones", "Vacuna"))
    for empleado in range(len(empleados_lista)):
        # elem va desde el primer elemento hasta el ultimo sin incluir el departamento
        for elem in range(len(empleados_lista[empleado]) - 1):
            # Dependiendo del el indice, es la cantidad de espacios hacia a la izquierda que agregamos. Para esto usamos las siguientes condiciones.
            if elem == 0:
                print("{:<8}".format(empleados_lista[empleado][elem]), end=" ")
            elif elem == 1:
                print("{:<25}".format(empleados_lista[empleado][elem]), end=" ")
            elif elem < 5:
                print("{:<10}".format(empleados_lista[empleado][elem]), end=" ")
            # Si elem es mayor a 5 aplicaremos el mismo formato para las condiciones ("diabetes", "hipertensión","corazon", "cancer", "tabaquismo", "vacuna")
            else:
                # Si el dato es igual a uno agregamos la condicion correspondiente en la lista de condiciones, de lo contrario solo se pondra una linea.
                if empleados_lista[empleado][elem] == "1":
                    print("{:<15}".format(condiciones[elem - 5]), end=" ")
                    condiciones_n[elem - 5] += 1
                else:
                    print("{:<15}".format("____________"), end=" ")
        print()

    # Calcular el porcentaje de empleados con cierta enfermedad o condicion
    for cant in condiciones_n:
        try:
            condiciones_frec.append(
                round((cant / len(empleados_lista)) * 100, 2))
        except ZeroDivisionError:
            break
    # Mostramos todos los datos calculados y almacenados en las listas
    print("{:<15} {:^8} {:^20}".format(
        "\nCondición", "Cantidad", "Porcentaje"))
    for con, can, frec in zip(condiciones, condiciones_n, condiciones_frec):
        print(f"{con:<15} {can:^8} {frec:>11}%")

    # Eliminamos todo en las listas condiciones_n y condiciones_frec para que no se acumule una suma cuando se vuelva a llamar la funcion.
    condiciones_n.clear()
    condiciones_frec.clear()
    empleados.clear()

def reporte_empleados_depto(archivo):
    leer_archivo(archivo)
    os.system('cls')
    while True:
        num_depto = input("Ingrese el número de departamento: ")
        if verificar_depto(num_depto):
            break
        print("El departamento ingresado no existe.")
    # Se llama la funcion que da el reporte de los empleados pero con la lista que devuelve la funcion verificar_depto()
    # Se eliminan los elementos de la lista antes de llamar la funcion de reporte
    empleados.clear()
    reporte_empleados(empleados_depto, archivo)
    print(f"Total de empleados en el departamento: {len(empleados_depto)}\n")
    # Al finalizar el reporte vaciamos la lista de empleados_depto()
    empleados_depto.clear()

def menu():
    print("""Sistema de bienestar Integral - Carlos David Sandoval

1. Alta de empleado
2. Calcular imc de empleado
3. Cambia información del empleado
4. Consulta un empleado
5. Reporte de todos los empleados
6. Reporte de empleados por departamento
7. Eliminar comandos anteriores
8. Salir""")
    return input("Teclea la opción: ")

def main():
    archivo = input('Ingrese el nombre del archivo con la extención ".csv": ')
    opcion = 0
    while opcion != 8:
        opcion = menu()
        try:
            opcion = int(opcion)
        except ValueError:
            print(f'"{opcion}" no es una opción valida. Intente de nuevo.')
            time.sleep(2)
            continue
        if opcion == 1:
            alta_empleado(archivo)
        elif opcion == 2:
            calcular_imc_empleado(archivo)
        elif opcion == 3:
            cambiar_info_empleado(archivo)
        elif opcion == 4:
            consultar_empleado(archivo)
        elif opcion == 5:
            # Enviamos como argumeto la lista de empleados
            reporte_empleados(empleados, archivo)
        elif opcion == 6:
            reporte_empleados_depto(archivo)
        elif opcion == 7:
            os.system('cls')
            continue
        elif opcion == 8:
            os.system('cls')
            break
        else:
            print(f'"{opcion}" no es una opción valida. Intente de nuevo.')
            time.sleep(2)
            os.system('cls')

if __name__ == "__main__":
    main()