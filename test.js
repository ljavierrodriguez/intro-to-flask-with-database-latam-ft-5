let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTExNTIwNiwianRpIjoiZGYyYjMyNDYtZDAwZS00OTlmLWE5MmUtYTdkYWZmYzc4Zjc2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3NTUxMTUyMDYsImNzcmYiOiI2ZTBiYjZlMS0wYTgwLTQxNzQtODhkNy1mMTk1YzFkZmJhNTciLCJleHAiOjE3NTUxMTg4MDZ9.16P6nFIs7T-clKbgGAgmPXJ8YWnBhqJlvYw76rAOGWc"
fetch('http://127.0.0.1:5000/profile', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Beader ' + token
    }
})
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error.message))