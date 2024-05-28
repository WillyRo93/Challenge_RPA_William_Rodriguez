import unittest
import os

# Importa todas las pruebas unitarias
from test_utils import TestUtils
# from test_image_downloader import TestImageDownloader
from test_excel_creator import TestExcelCreator
# from test_browser import TestNewsBrowser
# from test_news_scraper import TestNewsScraper

def run_tests():
    # Crea un objeto TestLoader para cargar todas las pruebas unitarias
    loader = unittest.TestLoader()

    # Agrega las pruebas unitarias de cada módulo al TestSuite
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    # suite.addTests(loader.loadTestsFromTestCase(TestImageDownloader))
    suite.addTests(loader.loadTestsFromTestCase(TestExcelCreator))
    # suite.addTests(loader.loadTestsFromTestCase(TestNewsBrowser))
    # suite.addTests(loader.loadTestsFromTestCase(TestNewsScraper))

    # Crea un objeto TextTestRunner para ejecutar las pruebas y mostrar los resultados
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Retorna True si todas las pruebas pasaron exitosamente, de lo contrario False
    return result.wasSuccessful()

if __name__ == "__main__":
    # Ejecuta las pruebas y obtiene el resultado
    tests_passed = run_tests()

    # Imprime el resultado de las pruebas
    if tests_passed:
        print("Todas las pruebas pasaron exitosamente.")
    else:
        print("Al menos una prueba falló.")
