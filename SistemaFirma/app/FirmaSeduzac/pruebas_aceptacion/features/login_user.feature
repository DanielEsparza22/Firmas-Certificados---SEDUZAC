Característica: Iniciar sesión en el sistema como usuario normal
    Como usuario quiero poder iniciar sesión en el sistema
    de tal manera que pueda acceder a las funciones para firmar certificados

    Escenario: Inicio de sesión exitoso
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario "Daniel" y mi contraseña "daniel123@"
        Cuando presiono el boton de Ingresar
        Entonces puedo ver mi nombre de usuario "Daniel" en la barra de navegacion principal

    Escenario: Inicio de sesión fallido
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "Daniel" y una contraseña incorrecta "daniel123"
        Cuando presiono el boton de Ingresar
        Entonces puedo ver el mensaje de error "Datos incorrectos."