import unittest
import requests
import psycopg2
from time import sleep
import json
from pathlib import Path
import sys
import asyncio

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'airport_service/app'))
sys.path.append(str(BASE_DIR / 'status_service/app'))

from airport_service.app.main import service_alive as service_alive1
from status_service.app.main import service_alive as service_alive2


class TestIntegration(unittest.TestCase):

    def test_airport_service_connection(self):
        r = asyncio.run(service_alive1())
        self.assertEqual(r, {'message': 'service alive'})

    def test_status_service_connection(self):
        r = asyncio.run(service_alive2())
        self.assertEqual(r, {'message': 'service alive'})


if __name__ == '__main__':
    unittest.main()
