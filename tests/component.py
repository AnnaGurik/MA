import requests
import unittest

airport_url = 'http://localhost:8000'
status_url = 'http://localhost:8001'
add_plane_url = f'{airport_url}/add_plane'
get_plane_by_name_url = f'{airport_url}/get_ticket_by_name'
get_plane_by_id_url = f'{airport_url}/get_ticket_by_id'


status_url = 'http://localhost:8001'
set_status_url = f'{status_url}/set_status'

plane = {
    "airplane_name": "Airbus_new",
    "num_seats": "1111",
}


class TestComponent(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_1_add_plane(self):
        res = requests.post(add_plane_url, json=plane)
        self.assertEqual(res, "Success")

    # def test_2_test_plane_get(self):
    #     res = requests.get(f"{get_plane_by_id_url}?plane_id=1").json()
    #     self.assertEqual(res['passenger_name'], "test")
    #     self.assertEqual(res['passport'], "11111")
    #     self.assertEqual(res['id_airplane'], 1)
    #     self.assertEqual(res['direction'], "Moscow")
    #
    # def fetch_tickets(self):
    #     res = requests.get(get_tickets_url)
    #     self.assertTrue(res != "Cant access database!")


if __name__ == '__main__':
    unittest.main()
