#!/usr/bin/env python3



import argparse

import sys

import os

import csv

from datetime import datetime



def es_valor_nulo(valor):

    if valor is None:

        return True



    if isinstance(valor, str) and valor.strip() == "":

        return True



    return False



def es_numerico(valor):

    try:

        float(str(valor).replace(",", "").strip())

        return True

    except (ValueError, TypeError):

        return False



def es_fecha(valor):

    try:

        datetime.strptime(str(valor).strip(), "%Y-%m-%d")

        return True

    except ValueError:

        return False



def es_booleano(valor):

    v = str(valor).strip().lower()



    return v in {

        "true", "false",

        "yes", "no",

        "si", "1", "0",

        "t", "f"

    }



def inferir_tipo(valores):

    no_nulos = [v for v in valores if not es_valor_nulo(v)]



    if not no_nulos:

        return "texto"



    total = len(no_nulos)

    umbral = 0.8



    n_fechas = sum(1 for v in no_nulos if es_fecha(v))

    n_booleanos = sum(1 for v in no_nulos if es_booleano(v))

    n_numericos = sum(1 for v in no_nulos if es_numerico(v))



    if n_fechas / total >= umbral:

        return "fecha"



    if n_booleanos / total >= umbral:

        return "booleano"



    if n_numericos / total >= umbral:

        return "numerico"



    return "texto"



def perfilar_columna(nombre, valores):

    total = len(valores)



    nulos = sum(

        1 for v in valores

        if es_valor_nulo(v)

    )



    no_nulos = [

        v for v in valores

        if not es_valor_nulo(v)

    ]



    unicos = len(set(no_nulos))



    ejemplo = no_nulos[0] if no_nulos else "N/A"



    pct_nulos = (

        nulos / total * 100

        if total > 0 else 0.0

    )



    pct_unicos = (

        unicos / total * 100

        if total > 0 else 0.0

    )



    return {

        "nombre_columna": nombre,

        "tipo_inferido": inferir_tipo(valores),

        "total_registros": total,

        "valores_nulos": nulos,

        "porcentaje_nulos": round(pct_nulos, 2),

        "valores_unicos": unicos,

        "porcentaje_unicos": round(pct_unicos, 2),

        "ejemplo_valor": ejemplo

    }



def leer_csv(ruta):

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:

        lector = csv.reader(archivo)



        filas = list(lector)



    if not filas:

        return [], []



    encabezados = filas[0]

    datos = filas[1:]



    return encabezados, datos



def escribir_csv(ruta, perfiles):

    columnas = [

        "nombre_columna",

        "tipo_inferido",

        "total_registros",

        "valores_nulos",

        "porcentaje_nulos",

        "valores_unicos",

        "porcentaje_unicos",

        "ejemplo_valor"

    ]



    os.makedirs(

        os.path.dirname(ruta) or ".",

        exist_ok=True

    )



    with open(ruta, "w", encoding="utf-8", newline="") as archivo:

        escritor = csv.writer(archivo)



        escritor.writerow(columnas)



        for p in perfiles:

            escritor.writerow([

                p["nombre_columna"],

                p["tipo_inferido"],

                p["total_registros"],

                p["valores_nulos"],

                f"{p['porcentaje_nulos']:.2f}",

                p["valores_unicos"],

                f"{p['porcentaje_unicos']:.2f}",

                p["ejemplo_valor"]

            ])



def main():

    parser = argparse.ArgumentParser(

        description="Perfilador de Datasets CSV"

    )



    parser.add_argument(

        "--input",

        "-i",

        required=True,

        help="Ruta al archivo CSV de entrada"

    )



    parser.add_argument(

        "--output",

        "-o",

        required=True,

        help="Ruta para el reporte CSV de salida"

    )



    args = parser.parse_args()



    try:

        print(f"Analizando dataset: {args.input}...")



        encabezados, filas = leer_csv(args.input)



        if not encabezados:

            print(

                "Error: El archivo está vacío o no tiene formato válido."

            )

            sys.exit(1)



        perfiles = []



        for i, nombre_col in enumerate(encabezados):

            valores = [

                fila[i] if i < len(fila) else ""

                for fila in filas

            ]



            perfiles.append(

                perfilar_columna(nombre_col, valores)

            )



        escribir_csv(args.output, perfiles)



        print(f"Éxito: Reporte generado en {args.output}")



        print(

            f"Columnas procesadas: {len(encabezados)} | "

            f"Registros: {len(filas)}"

        )



    except FileNotFoundError:

        print("Error: Archivo de entrada no encontrado.")

        sys.exit(1)



    except PermissionError:

        print("Error: Permisos insuficientes.")

        sys.exit(1)



    except Exception as error:

        print(f"Error crítico: {error}")

        sys.exit(1)



if __name__ == "__main__":

    main() 

