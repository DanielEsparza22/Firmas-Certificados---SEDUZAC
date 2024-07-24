import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given(u'selecciono del menu la opción de Certificaciones Totales')
def step_impl(context):
    context.driver.find_element(By.XPATH, "/html/body/div[1]/aside/div/div[4]/div/div/nav/ul/li[2]/a").click()
    time.sleep(2)


@given(u'selecciono la opción de Nuevo certificado')
def step_impl(context):
    context.driver.find_element(By.XPATH, "/html/body/div[1]/aside/div/div[4]/div/div/nav/ul/li[2]/ul[1]/li/a").click()
    time.sleep(2)


@given(u'escribo la CURP del alumno que quiero buscar "{curp}"')
def step_impl(context,curp):
    context.driver.find_element(By.NAME, "curp").send_keys(curp)
    time.sleep(2)

@when(u'presiono el botón de Enviar')
def step_impl(context):
    context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/section[2]/form/div/button").click()
    time.sleep(2)

@then(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/section[2]/p")
    assert mensaje in div.text, f'No esta {mensaje} en {div.text}'

@then(u'puedo ver la tabla "{tabla}" con los datos del certificado')
def step_impl(context,tabla):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/section[2]/div/table")
    assert "CURP" in div.text, f'CURP no esta en {div.text}'