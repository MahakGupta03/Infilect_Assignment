import json
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_empty_matrix():
    # Test when the matrix is empty
    response = client.post("/largest_rectangle", json={"matrix": []})
    assert response.status_code == 400
    assert "detail" in response.json()



def test1_find_largest_rectangle():
    # Test valid input
    matrix = [  [1, 1, 1, 0, 1, -9],
                [1, 1, 1, 1, 2, -9],
                [1, 1, 1, 1, 2, -9],
                [1, 0, 0, 0, 5, -9],
                [5, 0, 0, 0, 5]]
    response = client.post("/largest_rectangle", json={"matrix": matrix})
    assert response.status_code == 200
    result = response.json()
    assert result == [1,8]

    # Test invalid input
    response = client.post("/largest_rectangle", json={})
    assert response.status_code == 400
    assert "detail" in response.json()

def test2_find_largest_rectangle():
    # Test valid input
    matrix = [[1, 0, 1], [1, 1, 0], [1, 0, 1]]
    response = client.post("/largest_rectangle", json={"matrix": matrix})
    assert response.status_code == 200
    result = response.json()
    assert result == [1,3]

    # Test invalid input
    response = client.post("/largest_rectangle", json={})
    assert response.status_code == 400
    assert "detail" in response.json()

def test3_find_largest_rectangle():
    # Test valid input
    matrix = [ [9, 2, 7, 8, 0], [9, 7, 1, 1], [5, 9, 7, 1], [6, 4, 7]]
    response = client.post("/largest_rectangle", json={"matrix": matrix})
    assert response.status_code == 200
    result = response.json()
    assert result == [9,2]

    # Test invalid input
    response = client.post("/largest_rectangle", json={})
    assert response.status_code == 400
    assert "detail" in response.json()
