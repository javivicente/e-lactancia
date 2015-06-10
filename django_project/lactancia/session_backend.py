# Estas lineas de codigo impiden que el key id de una sesion cambie
# cuando el usuario pasa de ser anonimo a estar registrado/logueado
from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        pass
