Característica: Guardar Datos de Certificacion Total
    Como usuario quiero poder guardar los datos de certificación del alumno 
    para poder firmar el certificado.

    Escenario: Datos guardados correctamente
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono del menu la opción de Certificaciones Totales
        Y selecciono la opción de Nuevo certificado
        Y escribo la CURP del alumno que quiero buscar "RUHN890705HZSZRX05"
        Y presiono el botón de Enviar
        Y veo el mensaje "No se encontró el certificado"
        Y escribo la fecha de certificacion "23/07/2024"
        Cuando presiono el boton de Guardar Datos
        Entonces puedo ver el mensaje de exito de guardado de certificado total "Datos guardados correctamente."

    Escenario: Error al guardar los datos
        Dado que ingreso al sistema "http://192.168.33.10:8001/"
        Y escribo mi nombre de usuario de administrador "admin" y mi contraseña "admincert123"
        Y presiono el boton de Ingresar
        Y selecciono del menu la opción de Certificaciones Totales
        Y selecciono la opción de Nuevo certificado
        Y escribo la CURP del alumno que quiero buscar "AAAV881120MZSDGR06"
        Y presiono el botón de Enviar
        Y veo el mensaje "No se encontró el certificado"
        Y escribo la fecha de certificacion "23/07/2024"
        Cuando presiono el boton de Guardar Datos
        Entonces puedo ver el mensaje de error de guardado de certificado total "Error al guardar. Verifique los datos."