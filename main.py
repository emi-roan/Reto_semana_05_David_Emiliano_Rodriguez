import csv
import argparse
import os

def inferir_tipo(valores):
    """Determina si una columna es numérica, fecha o texto basado en un umbral del 80%."""
    # Filtrar valores nulos (cadenas vacías)
    no_nulos = [v.strip() for v in valores if v.strip() != ""]
    if not no_nulos:
        return "texto"
    
    total_no_nulos = len(no_nulos)
    conteo_num = 0
    conteo_fecha = 0

    for v in no_nulos:
        # Intento de detección numérica
        try:
            float(v)
            conteo_num += 1
            continue
        except ValueError:
            pass
        
        # Intento de detección de fecha (formato simple YYYY-MM-DD o similar con guiones)
        if v.count('-') == 2 or v.count('/') == 2:
            conteo_fecha += 1

    # Aplicar regla del 80%
    if (conteo_num / total_no_nulos) >= 0.8:
        return "numero"
    elif (conteo_fecha / total_no_nulos) >= 0.8:
        return "fecha"
    else:
        return "texto"

def procesar_csv(ruta_entrada, ruta_salida):
    if not os.path.exists(ruta_entrada):
        print(f"Error: El archivo {ruta_entrada} no existe.")
        return

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo_in:
        lector = csv.DictReader(archivo_in)
        campos = lector.fieldnames
        filas = list(lector)
        total_filas = len(filas)

    resultado = []

    for columna in campos:
        valores = [f[columna] for f in filas]
        
        # 1. Contar nulos (solo cadenas vacías, '0' cuenta como dato)
        nulos = sum(1 for v in valores if v.strip() == "")
        porc_nulos = round((nulos / total_filas) * 100, 2)
        
        # 2. Valores únicos
        unicos = len(set(v for v in valores if v.strip() != ""))
        porc_unicos = round((unicos / total_filas) * 100, 2)
        
        # 3. Inferir tipo
        tipo = inferir_tipo(valores)

        resultado.append({
            "nombre_columna": columna,
            "tipo_inferido": tipo,
            "total_registros": total_filas,
            "valores_nulos": nulos,
            "porcentaje_nulos": porc_nulos,
            "valores_unicos": unicos,
            "porcentaje_unicos": porc_unicos
        })

    # Guardar reporte
    with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_out:
        escritor = csv.DictWriter(archivo_out, fieldnames=resultado[0].keys())
        escritor.writeheader()
        escritor.writerows(resultado)
    
    print(f"Reporte generado con éxito en: {ruta_salida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perfilador automático de datasets CSV.")
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV de entrada")
    parser.add_argument("--output", required=True, help="Ruta donde se guardará el reporte")
    
    args = parser.parse_args()
    procesar_csv(args.input, args.output)