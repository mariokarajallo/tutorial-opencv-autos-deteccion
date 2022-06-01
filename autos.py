import cv2
from cv2 import threshold
from cv2 import THRESH_BINARY
import numpy as np
import pandas as pd
from rastreador import *

# vamos a crear un objeto de seguimiento
seguimiento = Rastreador()

# Realizamos la lectura del video
cap = cv2.VideoCapture('avenida3.mp4')

# Vamos a realizar una deteccion de objetos con camara estable
# Cambiando el tamaño del historial podemos tener mejores resultados (camara estatica)
# Tambien modificaremos el umbral entre menor sea mas deteccion tendremos (Falsos positivos)

# extrae los objetos en movimiento de una camara estabale
# deja el fondo en negro y el objeto que se mueve en blanco
# history = son las veces que se procesa el fondo, mientras mas alto sea mejor se procesara y mejor detectara los objetos
# varThreshold = umbral, mientras menor sea mas detecciones tendremos
# nuestros substractos nos envia fondo negro pero con algunos elementos grises (no queremos las sombras por ejemplo y para ello creamos una mascara)

deteccion = cv2.createBackgroundSubtractorMOG2(history=20000, varThreshold=100,detectShadows = False)

while True:
    ret, frame = cap.read()
    # redimencionamos el video, bajamos la calidad del video para visualizarlo bien
    frame = cv2.resize(frame, (1280, 720))

    # elegimos una zona de interes para contar el paso de autos
    # mascara con el finde que los objetos sea totalmente blancos y fondo sea negro
    zona = frame[200:500, 400:900]
    #zona = frame[23:103, 1233:332]

    # creamos una mascara a los fotogramas con el fin de que nuestros objetos
    # sean blancos y el fondo negro
    mascara = deteccion.apply(zona)
    # con este umbral eliminamos los pixeles grises y dejemoas solo los pixeles que pertenecen a nuestros objetos que estan totalmente blancos
    # (es como una linea que de la mitad para arriba lo deja blanco y la mitad para abajo negro )
    #
    _, mascara = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)
    # extraemos los contornos de la mascara y los detectamos para dibujar los rectangulos
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # lista donde vamos a almacenar las coordenas de los contornos
    detecciones = []

    # Dibujamos todos los contornos en frame, de azul claro con 2 de grosor
    for cont in contornos:
        # eliminamos los contornos pequenos

        area = cv2.contourArea(cont)
        # extraemos el area de los contornos que son mas grandes para no contar con los objetos muy pequenos
        if area > 1000:  # si el area es mayor a 100 pixeles
            # cv2.drawContours(zona,[cont],-1,(255,255,0),2)
            x, y, ancho, alto = cv2.boundingRect(cont)
            # dibujamos el rectangulo
            cv2.rectangle(zona, (x, y), (x+ancho, y+alto), (0, 255, 0), 2)
            # almacenamos la informacion de las detecciones
            detecciones.append([x, y, ancho, alto])


    # seguimiento de los objetos
    # una vez detectado los bordes y dibujados debemos de hacer el rastreo
    info_id = seguimiento.rastreo(detecciones)
    
    for inf in info_id:
        x, y, ancho, alto, id = inf
        # colocamos el id (numero de objeto) arriba del objeto detectado
        cv2.putText(zona, "Movil "+str(id), (x, y - 15),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        # dibujamos el rectangulo
        cv2.rectangle(zona, (x, y), (x + ancho, y + alto), (0, 255, 0), 3)
        

    print("Coordenas X-Y-W-H-ID :",info_id)  # muestra las coordenas x,y,ancho,alto y el id
    #guardamos los datos obtenidos en un archivo del tipo csv
    
    
    cv2.imshow('Zona de Interes', zona)
    cv2.imshow('Carretera', frame)
    cv2.imshow('Mascara', mascara)

    key = cv2.waitKey(5)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
