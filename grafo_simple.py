#/usr/bin/python2
#-*- encoding:utf-8 -*-


#Almacen de triplas.

import csv

class GrafoSimple:
    def __init__(self):
        '''Constructor que crea los tres índices que contendrá el almacén'''
        #El índice usa diccionarios que contienen diccionarios que contienen
        #conjuntos
        self._spo = {}
        self._pos = {}
        self._osp = {}


    def agrega(self, (suj, pre, obj)):
        '''permuta el sujeto, predicado y objeto para concordar con el orden
        de cada índice'''
        self._agrega_al_ind(self._spo, suj, pre, obj)
        self._agrega_al_ind(self._pos, pre, obj, suj)
        self._agrega_al_ind(self._osp, obj, suj, pre)


    def _agrega_al_ind(self, ind, a, b, c):
        '''Agrega los términos al índice y crea un diccionario y un conjunto
        si los términos no se encuentran ya en el índice.'''
        if a not in ind:
            ind[a] = {b:set([c])}
        else:
            if b not in ind[a]:
                ind[a][b] = set([c])
            else:
                ind[a][b].add(c)


    def elimina(self, (suj, pre, obj)):
        '''Localiza triplas que concuerdan con un patrón, las permuta y eli-
        mina de cada índice'''
        triplas = list(self.triplas((suj, pre, obj)))
        for (sinSuj, sinPre, sinObj) in triplas:
            self._elim_del_ind(self._spo, sinSuj, sinPre, sinObj)
            self._elim_del_ind(self._pos, sinPre, sinObj, sinSuj)
            self._elim_del_ind(self._osp, sinObj, sinSuj, sinPre)


    def _elim_del_ind(self, ind, a, b, c):
        '''Recorre el índice. Limpia los diccionarios y conjuntos vacíos.
        Elimina los términos de una tripla'''
        try:
            bs = ind[a]
            conj_c = bs[b]
            conj_c.remove(c)
            if len(conj_c) == 0:
                del bs[b]

        except KeyError:
            pass
    

    def carga(self, archivo):
        '''Metodo para cargar las triplas de un archivo csv. Requiere el mó-
        dulo "csv".'''
        f = open(archivo, "rb")
        lector = csv.reader(f)

        for suj, pre, obj in lector:
            suj = unicode(suj, "UTF-8")
            pre = unicode(pre, "UTF-8")
            obj = unicode(obj, "UTF-8")
            self.agrega((suj, pre, obj))

        f.close()

    
    def guarda(self, archivo):
        '''Metodo para guardar las triplas a un archivo csv. Requiere el módu-
        lo "csv".'''
        f = open(archivo, "wb")
        escritor = csv.writer(f)

        for suj, pre, obj in self.triplas((None, None, None)):
            escritor.writerow([suj.encode("UTF-8"), pre.encode("UTF-8"),
                obj.encode("UTF-8")])
        
        f.close()

#Consultas. para consultar se toma una patrón (sujeto, predicado, objeto) y
#regresa las triplas que concuerdan con el patrón. Los términos en la tripla
#puestos como None, son tratados como comodines.
    def triplas(self, (suj, pre, obj)):
        '''Determina qué indice usar basado en los términos que fueron omiti-
        dos. Itera sobre el indice correcto y devuelve las triplas que con-
        cuerdan con el patrón.'''
        #Revisa qué términos están presentes para usar el índice correcto:
        try:
            if suj != None:
                if pre != None:
                    #suj pre obj
                    if obj != None:
                        if obj in self._spo[suj][pre]:
                            yield (suj, pre, obj)
                    #suj pre None:
                    else:
                        for reg_obj in self._spo[suj][pre]:
                            yield (suj, pre, reg_obj)
                else:
                    #suj None obj
                    if obj != None:
                        for reg_pre in self._osp[obj][pre]:
                            yield (suj, reg_pre, obj)
                    #suj None None
                    else:
                        for reg_pre, conj_obj in self._spo[suj].items():
                            for reg_obj in conj_obj:
                                yield (suj, reg_pre, reg_obj)
            else:
                if pre != None:
                    #None pre obj
                    if obj != None:
                        for reg_suj in self._pos[pre][obj]:
                            yield (reg_suj, pre, obj)
                    #None pre None
                    else:
                        for reg_obj, conj_suj in self._pos[pre].items():
                            for reg_suj in conj_suj:
                                yield (reg_suj, pre, reg_obj)
                else:
                    #None None obj
                    if obj != None:
                        for reg_suj, conj_pre in self._osp[obj].items():
                            for reg_pre in conj_pre:
                                yield (reg_suj, reg_pre, obj)
                    #None None None
                    else:
                        for reg_suj, conj_pre in self._spo.items():
                            for reg_pre, conj_obj in conj_pre.items():
                                for reg_obj in conj_obj:
                                    yield (reg_suj, reg_pre, reg_obj)
        #La excepción KeyError sucede si un término de la consulta no se en-
        #cuentra en el índice. En este caso no hacemos nada
        except KeyError:
            pass


    def valor(self, suj = None, pre = None, obj = None):
        '''Consulta sólo un valor de una sola tripla'''
        for reg_suj, reg_pre, reg_obj in self.triplas((suj, pre, obj)):
            if suj is None:
                return reg_suj
            if pre is None:
                return reg_pre
            if obj is None:
                return reg_obj
            break
        return None


def main():
    from grafo_simple import GrafoSimple
    mg = GrafoSimple()
    mg.agrega(('blade_runner', 'name', 'Blade Runner'))
    mg.agrega(('blade_runner', 'directed_by', 'ridley_scott'))
    mg.agrega(('ridley_scott', 'name', 'Ridley Scott'))
    mg.agrega(('e.t.', 'name', 'E.T'))
    mg.agrega(('e.t.', 'directed_by', 'steven_spilberg'))
    mg.agrega(('steven_spilberg', 'name', 'Steven Spilberg'))
    mg.agrega(('harrison_ford', 'starred', 'blade_runner'))
    mg.agrega(('harrison_ford', 'starred', 'indina_jones'))
    mg.agrega(('indiana_jones', 'directed_by', 'steven_spilberg'))
    mg.agrega(('harrison_ford', 'name', 'Harrison Ford'))
    mg.agrega(('indiana_jones', 'name', 'Indiana Jones'))
    print list(mg.triplas(('blade_runner', 'directed_by', None)))


if __name__ == "__main__":
    main()

