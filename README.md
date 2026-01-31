# Capturadora Presentaciones y transformador a PDF
## Requisitos previos
- python 3.14+

## Referecias
- IA 
- Stackoverflow

## Instalacion y funcionamiento
Librerias a instalar
```
pip install PyMuPDF
pip install pyautogui\

```

## Ejecución
1. Abre la presentación en pantalla completa
2. Ejecuta el fichero de CapturadoraPresentaciones.py, pero no lo inicies
3. Mira cuantas Diapositivas/Slides tiene la presentación y en el apartado de configuración -> número de repeticiones indicas el numero de diapositivas
4. Inicializa la automatización y minimiza rapido la ventana de "Automatización de clicks", asegurate que el ratón esté en medio de la presentación
5. Si te equivocas en el numero de repeticiones, espera a que llegue a la ultima slide, espera 10s vuelve a la ventana y cancela 
*Recomendación: si tienes dos pantallas es mejor para visualizar la ventana mientras va ejecutandose*
6. Al finalizar se habrá generado una carpeta screenshots con las imagenes de las slides
7. Abre el fichero de PNGaPDF.py y cambia la dirección de la carpeta destino por la dirección de la carpeta de las screenshots recien generada y el nombre del archivo que tu prefieras, siempre finalizado por .pdf
8. ejecuta el fichero y ya tienes tu PDF