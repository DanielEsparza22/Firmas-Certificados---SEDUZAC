import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given(u'que ingreso al sistema "{url}"')
def step_ingresar_sistema(context,url):
    context.driver = webdriver.Chrome()
    context.driver.get(url)
    time.sleep(2)

@given(u'escribo mi nombre de usuario de administrador "{username}" y mi contraseña "{password}"')
def step_impl(context, username, password):
    user = context.driver.find_element(By.NAME, "username")
    user.send_keys(username)
    time.sleep(2)
    contra = context.driver.find_element(By.NAME, "password")
    contra.send_keys(password)
    time.sleep(2)

@given(u'escribo mi nombre de usuario de administrador "{username}" y una contraseña incorrecta "{pass_incorrect}"')
def step_impl(context, username, pass_incorrect):
    user = context.driver.find_element(By.NAME, "username")
    user.send_keys(username)
    time.sleep(2)
    contra = context.driver.find_element(By.NAME, "password")
    contra.send_keys(pass_incorrect)
    time.sleep(2)

@when(u'presiono el boton de Ingresar')
def step_impl(context):
    btn_ingresar = context.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/form/div[3]/div/button")
    btn_ingresar.click()
    time.sleep(2)

@then(u'puedo ver mi nombre de usuario "{username}" en la barra de navegacion principal')
def step_impl(context, username):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/nav")
    time.sleep(2)
    assert f'Bienvenido {username}' in div.text, f'No esta {username} en {div.text}'

@then(u'puedo ver el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    div = context.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div")
    time.sleep(1)
    assert mensaje in div.text, f'No esta el mensaje de error {mensaje}'