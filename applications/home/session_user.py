class User:
    def __init__(self, request):
        self.__request = request
        self.__session = self.__request.session
        respuesta = self.__session.get("user", False)

        if not respuesta:
            respuesta = self.__session["user"] = {}
        self.__respuesta = respuesta

    def __save(self):
        self.__session["user"] = self.__respuesta
        self.__session.modified = True

    def get(self):
        return self.__respuesta.copy()


    def clear(self, user):
        if str(user.id) in self.__respuesta.keys():
            del self.__respuesta[str(user.id)]
            self.__save()

    # Inicio y fin de sesion

    def logout_user(self):
        return self.__session.pop("user", False) #self.session.flush()

    def login_user(self, user):
        if "data" not in self.__respuesta.keys():
            self.__respuesta["data"] = {
                "id": user.id,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "edad": user.edad
            }
            self.__save()

    ##########

    # Info del juego
    def add(self, **kwargs):
        if "data" in self.__respuesta.keys():
            self.__respuesta["player"] = {
                "puntos" : kwargs.get("puntos"),
                "actual": kwargs.get("actual"),
                "next": kwargs.get("next")
            }
            self.__save()



    def update(self,**kwargs):
        if "data" in self.__respuesta.keys():
            if self.__respuesta["player"]:
                self.__respuesta["player"]["puntos"] = kwargs.get("puntos")
                self.__respuesta["player"]["actual"] = kwargs.get("actual")
                self.__respuesta["player"]["next"] = kwargs.get("next")

                self.__save()
