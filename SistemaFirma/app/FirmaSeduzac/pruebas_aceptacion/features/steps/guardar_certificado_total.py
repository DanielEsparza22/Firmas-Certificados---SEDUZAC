import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given(u'presiono el botón de Enviar')
def step_impl(context):
    context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/section[2]/form/div/button").click()
    time.sleep(2)

@given(u'veo el mensaje "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/section[2]/p")
    assert mensaje in div.text, f'{mensaje} no esta en {div.text}'
    time.sleep(1)

@given(u'escribo la fecha de certificacion "{fecha}"')
def step_impl(context,fecha):
    context.driver.find_element(By.NAME,"fecha_certificacion").send_keys(fecha)
    time.sleep(1)


@when(u'presiono el boton de Guardar Datos')
def step_impl(context):
    context.driver.find_element(By.NAME, "obtener_registros").click()
    time.sleep(2)

@then(u'puedo ver el mensaje de exito de guardado de certificado total "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div")
    assert mensaje in div.text, f'{mensaje} no en {div.text}'

@then(u'puedo ver el mensaje de error de guardado de certificado total "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div")
    assert mensaje in div.text, f'{mensaje} no en {div.text}'