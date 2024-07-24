Característica: Verificar certificado total
    quiero comprobar mediante la CURP del alumno si este ya cuenta con certificado 
    total o no para saber si se debe firmar uno nuevo.

    Escenario: No existe certificado
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono del menu la opción de Certificaciones Totales
        Y selecciono la opción de Nuevo certificado
        Y escribo la CURP del alumno que quiero buscar "RUHN890705HZSZRX05"
        Cuando presiono el botón de Enviar
        Entonces puedo ver el mensaje "No se encontró el certificado"

    Escenario: Ya existe el certificado
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono del menu la opción de Certificaciones Totales
        Y selecciono la opción de Nuevo certificado
        Y escribo la CURP del alumno que quiero buscar "RUHN890705HZSZRX05"
        Cuando presiono el botón de Enviar
        Entonces puedo ver la tabla "Certificado" con los datos del certificado