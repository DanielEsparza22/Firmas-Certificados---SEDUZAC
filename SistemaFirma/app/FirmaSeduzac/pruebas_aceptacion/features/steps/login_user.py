import time
from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given(u'escribo mi nombre de usuario "{username}" y mi contraseña "{password}"')
def step_impl(context, username, password):
    user = context.driver.find_element(By.NAME, "username")
    user.send_keys(username)
    time.sleep(2)
    contra = context.driver.find_element(By.NAME, "password")
    contra.send_keys(password)
    time.sleep(2)