import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@then(u'puedo ver la lista de tipos de certificaciones en el Menu de opciones')
def step_impl(context):
    div = context.driver.find_element(By.XPATH, "/html/body/div[1]/aside/div/div[4]/div/div")
    time.sleep(1)
    assert "MENÚ" in div.text, f'MENÚ no esta en {div.text}'