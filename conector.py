import fdb
import json
import os

# 1. Cargar la librería (Como ya lo logramos)
fdb.load_api(os.path.abspath('fbclient.dll'))

ruta_db = r'C:\Users\GCQMZO-LuisGiron\OneDrive - 3PL SERVICES\Escritorio\CASA.GDB' # Pon tu ruta real

try:
    con = fdb.connect(host='localhost', database=ruta_db, user='SYSDBA', password='masterkey', charset='UTF8')
    cursor = con.cursor()

    # 2. Tu SQL tal cual lo pasaste
    sql = """
    SELECT NUM_PEDI, NUM_REFE, CVE_IMPO, TIP_PEDI, FEC_ENTR, DIA_PAGO, VAL_COME, TOT_EFEC
    FROM SAAIO_PEDIME 
    WHERE CVE_IMPO = '5776' 
    AND EXTRACT(YEAR FROM FEC_ENTR) = 2025 
    AND EXTRACT(MONTH FROM FEC_ENTR) = 11 
    AND FIR_ELEC <> ''
    ORDER BY NUM_PEDI, FEC_ENTR
    """
    
    cursor.execute(sql)
    registros = cursor.fetchall()

    # 3. Formatear los datos para la web
    datos_web = []
    for r in registros:
        datos_web.append({
            "pedimento": r[0].strip() if r[0] else "",
            "referencia": r[1].strip() if r[1] else "",
            "tipo": r[3].strip() if r[3] else "",
            "fecha": str(r[4]), # Convertimos fecha a texto para JSON
            "valor_comercial": float(r[6]) if r[6] else 0.0,
            "total_efectivo": float(r[7]) if r[7] else 0.0
        })

    # 4. Crear el archivo JSON
    with open('busqueda_actual.json', 'w', encoding='utf-8') as f:
        json.dump(datos_web, f, indent=4, ensure_ascii=False)

    print(f"--- PROCESO TERMINADO ---")
    print(f"Se encontraron {len(datos_web)} pedimentos con firma.")
    print(f"Archivo 'busqueda_actual.json' listo para la web.")

    con.close()

except Exception as e:
    print(f"Error: {e}")