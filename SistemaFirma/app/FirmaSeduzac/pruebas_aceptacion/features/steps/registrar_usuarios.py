import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given(u'presiono el boton de Ingresar')
def step_impl(context):
    btn_ingresar = context.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/form/div[3]/div/button")
    btn_ingresar.click()
    time.sleep(2)


@given(u'selecciono la opción de Registrar Usuarios')
def step_impl(context):
    registrar = context.driver.find_element(By.XPATH, "/html/body/div[1]/nav/ul/li[3]/a")
    registrar.click()
    time.sleep(2)

@given(u'escribo el nombre del nuevo usuario "{user_nuevo}" y su contraseña "{contra}"')
def step_impl(context,user_nuevo,contra):
    context.driver.find_element(By.NAME,"username").send_keys(user_nuevo)
    time.sleep(2)
    context.driver.find_element(By.NAME, "password").send_keys(contra)
    time.sleep(2)

@given(u'escribo el nombre del nuevo usuario "{usuario}"')
def step_impl(context,usuario):
    context.driver.find_element(By.NAME,"username").send_keys(usuario)
    time.sleep(2)

@when(u'presiono el boton de Registrar')
def step_impl(context):
    context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/div/form/div[3]/div/button").click()
    time.sleep(4)

@then(u'puedo ver el mensaje de exito "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/ul/div")
    assert mensaje in div.text, f'{mensaje} no en {div.text}'

@then(u'puedo ver el mensaje de error de registro de usuario "{mensaje}"')
def step_impl(context,mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/div/div")
    assert mensaje in div.text, f'{mensaje} no en {div.text}'