Característica: Registrar un usuario nuevo en el sistema
    Como usuario administrador quiero resgistrar un usuario nuevo en el sistema
    para que acceda a las funcionalidades de firma de certificados

    Escenario: Registro de usuario correcto
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono la opción de Registrar Usuarios
        Y escribo el nombre del nuevo usuario "Maria" y su contraseña "maria123@"
        Cuando presiono el boton de Registrar
        Entonces puedo ver el mensaje de exito "Maria se registró de manera exitosa"

    Escenario: Registro de usuario incorrecto
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono la opción de Registrar Usuarios
        Y escribo el nombre del nuevo usuario "Jose"
        Cuando presiono el boton de Registrar
        Entonces puedo ver el mensaje de error de registro de usuario "Hubo un error con el registro. Por favor, revisa los campos."