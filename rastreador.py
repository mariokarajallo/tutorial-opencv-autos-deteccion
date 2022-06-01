import math
import pandas as pd
# creamos una clase que sea nuestro rastreador


class Rastreador:
    # inicializamos las variables
    def __init__(self):
        # aca vamos a almacenar las posiciones centrales de los objetos
        # para saber que ese objeto ya lo detectamos
        self.centro_puntos = {}
        # almacenar las pocisiones centrasles de los objetos
        # contador de objetos, numero que aparece sobre los objetos
        self.id_count = 1

    def rastreo(self, objetos):
        # lista donde almacenamos los objetos identificados
        objeto_identificado = []

        # obtenmos el punto central de nuevo objeto detectado
        for rect in objetos:
            # recibe las coordenadas x,y ancho y alto con el fin de extraer el punto central
            x, y, w, h = rect
            cx = (x+x+w)//2
            cy = (y+y+h)//2

            # miramos  si ese objeto ya fue detectado
            objeto_detectado = False
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 25:
                    self.centro_puntos[id] = (cx, cy)
                    print("Centro Puntos: ",self.centro_puntos)
                    objeto_identificado.append([x, y, w, h, id])
                    objeto_detectado = True
                    break

            # si detecta un nuevo objeto le asignamos el ID a ese objeto
            if objeto_detectado is False:
                self.centro_puntos[self.id_count] = (
                    cx, cy)  # almacenamos la coordenada x e y
                # agregamos el objeto con su ID
                objeto_identificado.append([x, y, w, h, self.id_count])
                # aumentamos el ID
                self.id_count = self.id_count + 1  

        print("Total identificados: ",self.id_count)
        #guardamos el contador de objetos detectados a un archivo txt
        with open('datos.txt','r+') as myfile:
            data = myfile.read()
            myfile.seek(0)
            myfile.write(str(self.id_count)+","+"Lunes 28-05-2022")
            myfile.truncate()



        # limpiar la lista por puntos centrales para eliminar IDS que ya no se usan, por que estos nos consumen recursos y eso queremos evitar
        new_center_points = {}
        for obj_bb_id in objeto_identificado:
            _, _, _, _, object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center

        # actualizar lista con los ID no utilizados eliminados
        self.centro_puntos = new_center_points.copy()
        return objeto_identificado
