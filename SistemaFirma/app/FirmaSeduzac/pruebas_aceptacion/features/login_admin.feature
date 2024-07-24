Característica: Iniciar sesión en el sistema como administrador
    Como Administrador quiero poder iniciar sesión en el sistema
    de tal manera que tambien pueda acceder a funciones de administrador.

    Escenario: Inicio de sesión exitoso
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Cuando presiono el boton de Ingresar
        Entonces puedo ver mi nombre de usuario "admin" en la barra de navegacion principal

    Escenario: Inicio de sesión fallido
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y una contraseña incorrecta "admin123"
        Cuando presiono el boton de Ingresar
        Entonces puedo ver el mensaje de error "Datos incorrectos."