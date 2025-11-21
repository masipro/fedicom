class Ldap:
    async def autenticar(self, solicitud):
        # Dummy implementation
        if solicitud.usuario == 'ldapuser' and solicitud.clave == 'ldappass':
            return ['group1', 'group2']
        else:
            raise Exception("Invalid LDAP credentials")

ldap = Ldap()
