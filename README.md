Proyecto: Reto Semana 05 Asignatura: Programación para Ciencia de Datos

Institución: Escuela Superior de Cómputo (ESCOM) - IPN
Autor: David Emiliano Rodríguez Anduiza 

Descripción del Proyecto
En el flujo de trabajo de Ciencia de Datos, el Análisis Exploratorio de Datos (EDA) es el primer paso crítico. Este proyecto es una herramienta de línea de comandos (CLI) desarrollada en Python que automatiza el diagnóstico de calidad de cualquier archivo CSV.

El programa escanea el dataset columna por columna para inferir tipos de datos, detectar valores nulos y calcular métricas de unicidad, generando un reporte consolidado que sirve como punto de partida para la limpieza de datos.

Características Principales
Inferencia Estadística de Tipos: Clasifica columnas como numerico, fecha, booleano o texto mediante un umbral de confianza del 80%.

Diagnóstico de Calidad: Calcula el volumen y porcentaje de valores nulos (faltantes).

Análisis de Cardinalidad: Identifica la cantidad de valores únicos por columna.

Interfaz de Línea de Comandos (CLI): Implementación profesional mediante argparse para manejo de rutas de entrada y salida.

Resiliencia: Capacidad para procesar archivos con filas incompletas o datos ruidosos sin interrumpir la ejecución.

Lógica de Inferencia de Datos
Para determinar el tipo de una columna, el programa utiliza un sistema de mayoría simple optimizada:

Filtro de Nulos: Se ignoran celdas vacías para el cálculo del tipo.

Umbral del 80%: Si al menos el 80% de los datos válidos cumplen con un formato específico, se asigna ese tipo.

Orden de Prioridad:

Fecha: Formato ISO YYYY-MM-DD.

Booleano: Valores como True/False, 1/0, Si/No.

Numérico: Valores que pueden convertirse a flotantes (incluyendo manejo de comas).

Texto: Categoría por defecto si no se cumplen las anteriores.

Guía de Uso
Requisitos
Python 3.8 o superior.

No requiere librerías externas (Standard Library únicamente).

Ejecución
Usa los argumentos --input (o -i) para el archivo de origen y --output (o -o) para el destino del reporte:

Bash
python main.py --input data/ejemplo_ventas.csv --output outputs/perfil_ventas.csv
Formato del Reporte (Salida)
El archivo generado en outputs/ contendrá las siguientes métricas:

nombre_columna: Identificador original en el CSV.

tipo_inferido: Clasificación detectada (texto, numerico, fecha, booleano).

total_registros: Cantidad total de filas procesadas.

valores_nulos: Conteo de celdas vacías detectadas.

porcentaje_nulos: Proporción de datos faltantes (0.00% - 100.00%).

valores_unicos: Número de categorías o valores distintos.

ejemplo_valor: Muestra del primer dato válido encontrado.

Conclusión: 
De la Lógica a la Producción
El desarrollo de estos retos representa una evolución significativa en la mentalidad de un desarrollador orientado a la Ciencia de Datos. Mientras que los primeros ejercicios se enfocaron en la lógica de programación básica y estructuras de datos, la culminación en herramientas como el Perfilador de Datasets demuestra el dominio de tres pilares fundamentales:

Robustez y Calidad: La implementación de validadores y el manejo de excepciones aseguran que el código no solo "funcione", sino que sea capaz de procesar datos del mundo real, los cuales suelen ser ruidosos, incompletos o erróneos.

Modularidad y Escalabilidad: Pasar de scripts lineales a arquitecturas modulares (como en el sistema de inventario) permite que el software sea mantenible a largo plazo y que otros desarrolladores puedan colaborar en el mismo proyecto sin fricciones.

Automatización Profesional: La creación de interfaces de línea de comandos (CLI) transforma un simple script en una herramienta de producción reutilizable. Esto reduce el tiempo de exploración de datos y permite estandarizar procesos de diagnóstico que son vitales antes de cualquier entrenamiento de modelos de Machine Learning.

En resumen, estos retos no solo han servido para practicar la sintaxis de Python, sino para adoptar buenas prácticas de ingeniería de software que garantizan la reproducibilidad y la confiabilidad en cualquier flujo de análisis de datos profesional.
