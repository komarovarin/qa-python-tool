import pytest
from sys import platform
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

from steps import support_steps

# Описываем дополнительные опции командной строки
# --env - описываем окружение-стенд, на котором будет выполняться тестирование
# --browser - браузер, на котором будет выполняться тестирование
from Steps.support_steps import saveScreenshot


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     default="IFT_SB",
                     help='available environments: IFT_SB, IFT_GF, PSI_SB, PSI_GF',
                     choices=("IFT_SB", "IFT_GF", "PSI_SB", "PSI_GF")
                     )
    parser.addoption("--browser",
                     action="store",
                     default="Sber",
                     help='available environments: IE, Sber, Chrome, Edge',
                     choices=("IE", "Sber", "Chrome", "Edge")
                     )


# Фикстура окружения-стенда
@pytest.fixture(autouse=True, scope="session")
def env(pytestconfig):
    enironment = pytestconfig.getoption("env")
    yield enironment


# Фикстура браузера
@pytest.fixture(autouse=True, scope="session")
def browser(pytestconfig):
    browser = pytestconfig.getoption("browser")
    yield browser


# Фикстура драйвера для запуска браузера
@pytest.fixture(scope="function")
def driver(browser, request):
    try:
        driver = None
        print("Start driver")
        print("platform = ", platform)
        # print("platform = ", platform.system())
        # SberBrowser
        if browser == "Sber":
            options = webdriver.ChromeOptions()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors=yes")
            # Локально
            if platform == "win32":
                driver = webdriver.Chrome(r"sberbrowser_driver_3.0.0.0.exe", options=options)

            else:
                # Запуск в Moon
                capabilities = {
                    "browserName": "chrome",
                    "browserVersion": "3.1.10.0",
                    "acceptInsecureCerts": True,
                    "goog:chromeOptions": {
                        "args": ["no-sandbox"],
                        "binary": "/usr/bin/sberbrowser-browser"
                    },
                    "moon:options": {
                        "enableVNC": True,
                        "enableVideo": False,
                        "name": "MoonTest",
                        # "screenResolution": "1920x1080",
                        "sessionTimeout": "5m",
                    }
                }

                username = "XXXXXXXX"
                password = "XXXXXXXX"
                moonHost = "yourhost.ru"

                hub = 'http://{}:{}@{}/wd/hub'.format(
                    username, password, moonHost)
                print("moonHost = ", moonHost)
                driver = webdriver.Remote(
                    command_executor=RemoteConnection(hub, resolve_ip=False),
                    desired_capabilities=capabilities, options=options)
                print("driver.session_id = ", driver.session_id)

        # Internet Explorer
        elif browser == "IE":
            driver = webdriver.Ie()

        # Google Chrome
        elif browser == "Chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors=yes")
            # Локально
            if platform == "win32":
                driver = webdriver.Chrome("C:\Program Files (x86)\ChromeDriver\chromedriver.exe", options=options)
            else:
                # Запуск в Moon
                capabilities = {
                    "browserName": "chrome",
                    "browserVersion": "108.0",
                    "goog:loggingPrefs": {"performance": "ALL"},
                    "acceptInsecureCerts": True,
                    "goog:chromeOptions": {
                        "args": ["no-sandbox"]
                    },
                    # "add_Arguments": "--ignore-certificate-errors",
                    # "add_Arguments": "--ignore-ssl-errors=yes",
                    "moon:options": {
                        "enableVNC": True,
                        "enableVideo": False,
                        "name": "MoonTest",
                        # "screenResolution": "1024x768",
                        "sessionTimeout": "5m",
                    }
                }
                username = "XXXXXXXX"
                password = "XXXXXXXX"
                moonHost = "yourhost.ru"

                hub = 'http://{}:{}@{}/wd/hub'.format(
                    username, password, moonHost)
                print("moonHost = ", moonHost)
                driver = webdriver.Remote(
                    command_executor=RemoteConnection(hub, resolve_ip=False),
                    desired_capabilities=capabilities, options=options)
                print("driver.session_id = ", driver.session_id)

        # Google Chrome
        elif browser == "Edge":
            options = webdriver.ChromeOptions()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors=yes")
            # Локально
            if platform == "win32":
                driver = webdriver.Edge("./resources/drivers/msedgedriver.exe", options)
            else:
                # Запуск в Moon
                capabilities = {
                    "browserName": "MicrosoftEdge",
                    "browserVersion": "107.0",
                    "goog:loggingPrefs": {"performance": "ALL"},
                    "acceptInsecureCerts": True,
                    "ms:edgeOptions": {
                        "args": ["no-sandbox"]
                    },
                    "moon:options": {
                        "enableVNC": True,
                        "enableVideo": False,
                        "name": "MoonTest",
                        # "screenResolution": "1024x768",
                        "sessionTimeout": "5m",
                    }
                }
                username = "XXXXXXXX"
                password = "XXXXXXXX"
                moonHost = "yourhost.ru"

                hub = 'http://{}:{}@{}/wd/hub'.format(
                    username, password, moonHost)
                # hostname = 'http://teslaefs:CFrQsV6vT@moon-sw.apps.dev-gen.sigma.sbrf.ru/wd/hub'
                # hostname = 'http://teslaefs:CFrQsV6vT@moon-sw.sh1.dev-gen.delta.sbrf.ru/wd/hub'
                print("moonHost = ", moonHost)
                driver = webdriver.Remote(
                    command_executor=RemoteConnection(hub, resolve_ip=False),
                    desired_capabilities=capabilities, options=options)
                print("driver.session_id = ", driver.session_id)

        # Невозможный вариант, но здесь нужен else
        else:
            driver = webdriver.Firefox()
        # Чистим cookies
        driver.delete_all_cookies()
        yield driver

    finally:
        # Закрываем браузер
        if browser == "Chrome":
            support_steps.get_response_output(driver)
        print("Quit")
        # Локально
        if platform != "win32":
            driver.quit()
