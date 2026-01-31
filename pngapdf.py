import fitz  # PyMuPDF
import os
from math import ceil

carpeta_imagenes = r"C:\Users\....\Screenshots"
archivo_salida = "U1-S1.pdf"

def pngs_a_pdf_optimo(carpeta_imagenes, archivo_salida,
                      target_dpi=150,  # 150–200 suele ser buen balance
                      max_width_px=None, max_height_px=None):
    """
    Convierte PNG -> PDF optimizando tamaño:
    - Reescala cada imagen para aproximar target_dpi (si trae DPI) o a límites máximos.
    - Guarda con garbage=4 y deflate=True.
    """
    doc = fitz.open()

    archivos = sorted([f for f in os.listdir(carpeta_imagenes)
                       if f.lower().endswith(".png")])

    for nombre in archivos:
        ruta = os.path.join(carpeta_imagenes, nombre)
        img_doc = fitz.open(ruta)
        page_rect = img_doc[0].rect

        # 1) Obtener tamaño en px
        w_px = int(page_rect.width)
        h_px = int(page_rect.height)

        # 2) Calcular factor de reescalado
        #    Si max_width_px / max_height_px están definidos, limitamos por ahí.
        sx = sy = 1.0
        if max_width_px or max_height_px:
            if max_width_px:
                sx = min(sx, max_width_px / w_px)
            if max_height_px:
                sy = min(sy, max_height_px / h_px)
        # Si no se definieron límites, aproximamos a un tamaño "razonable" por DPI
        # (Asumimos 72 pt = 1 in en PDF; 1 px ≈ 1 pt por defecto, así que ajustamos)
        # Queremos que en PDF el "tamaño visual" no sea desproporcionado.
        # Usamos un factor por DPI relativo a 150 dpi (heurístico).
        base_dpi = 150
        scale_dpi = target_dpi / base_dpi
        sx = sy = min(sx, scale_dpi)

        # Evitar que suba de tamaño
        sx = min(sx, 1.0)
        sy = min(sy, 1.0)

        # 3) Renderizar pixmap reescalado (downsample)
        #    La matriz escala las dimensiones de rasterizado
        mat = fitz.Matrix(sx, sy)
        pix = img_doc[0].get_pixmap(matrix=mat, alpha=False)  # sin alfa -> menos peso
        img_doc.close()

        # 4) Crear página del tamaño del bitmap final (en puntos)
        page = doc.new_page(width=pix.width, height=pix.height)

        # 5) Insertar desde memoria (evita guardar temporal)
        page.insert_image(page.rect, stream=pix.tobytes("png"))  # mantiene compresión PNG
        # Si son capturas "fotográficas", ver opción B para JPEG

    # 6) Guardado optimizado
    doc.save(archivo_salida, garbage=4, deflate=True)
    doc.close()
    print(f"✅ PDF optimizado: {archivo_salida}")


pngs_a_pdf_optimo(carpeta_imagenes,archivo_salida,
                  target_dpi=150, max_width_px=1920, max_height_px=1920)


