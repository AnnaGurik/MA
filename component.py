import requests
import unittest
from datetime import datetime

airport_url = 'http://localhost:8000'
status_url = 'http://localhost:8001'
add_plane_url = f'{airport_url}/add_plane'
get_plane_by_name_url = f'{airport_url}/get_planes_by_name'
get_plane_by_id_url = f'{airport_url}/get_plane_by_id'


status_url = 'http://localhost:8001'
set_status_url = f'{status_url}/set_status'

plane = {
    "id": 77,
    "airplane_name": "Airbus_new",
    "num_seats": "1111",
    "status": "test",
    "manufacture_date": datetime.now().isoformat()
}


class TestComponent(unittest.TestCase):

    def test_1_add_plane(self):
        res = requests.post(add_plane_url, json=plane)
        self.assertEqual(res.text, '"Success"')

    def test_2_plane_get_by_id(self):
        res = requests.get(f"{get_plane_by_id_url}?plane_id=2").json()
        self.assertEqual(res['airplane_name'], "Airbus_new")
        self.assertEqual(res['num_seats'], 1111)
        self.assertEqual(res['status'], "test")

    def test_3_plane_get_by_name(self):
        res = requests.get(f"{get_plane_by_name_url}?plane_name=Airbus_new").json()
        self.assertEqual(res['airplane_name'], "Airbus_new")
        self.assertEqual(res['num_seats'], 1111)
        self.assertEqual(res['status'], "created")

    def test_4_set_status(self):
        res = requests.post(f"{set_status_url}?plane_id=2&status=test").json()
        self.assertEqual(res, "Success")


if __name__ == '__main__':
    unittest.main()
