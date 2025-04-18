from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_create_bus():
    response = client.post(
        "/buses/create/",
        json={
            'number': "AA220A",
            'company_name': 'string1',
            'terminal_id': '1',
            'route': 'string'
        },
    )
    assert response.status_code == 200
    assert type(response.json()) == int


def test_update_bus_by_id():
    response = client.put(
        "/buses/update/?bus_id=1",
        json={
            'number': "AA220A",
            'company_name': 'string1',
            'terminal_id': 1,
            'route': 'string'
        }
    )
    assert response.status_code == 200
    assert response.json() == {}


def test_read_bus_by_number():
    response = client.get(
        "/buses/get-by-number/?bus_number=AA220A",
    )
    assert response.status_code == 200
    assert response.json() == {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 1
    }

def test_read_buses_by_company_name():
    response = client.get(
        "/buses/get-by-company-name/?company_name=string1",
    )
    assert response.status_code == 200
    assert response.json() == [
        {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 1
    },
    {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 2
    },
    {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 3
    },
    {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 4
    },
    {
        "number": "AA220A",
        "company_name": "string1",
        "terminal_id": 1,
        "route": "string",
        "id": 16
    },
    ]