import requests


def patch_request_authorized():
    """example of authorized request"""
    url = 'http://localhost:8000/map/profile'
    # Headers for the request (assuming Token-based authentication)
    headers = {
        'Authorization': 'Token dbba18c0d149ddc4e7dd376b338085cb05187e07',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Data to update the 'country' field
    data = {
        'country': 'Czechia'  # New value for the 'country' field
    }
    # Send the PATCH request
    response = requests.patch(url, data=data, headers=headers)
    print(response.json())


def get_user_token():
    url = 'http://localhost:8000/api-token-auth/'
    data = {
        'username': 'matous',  # Replace with your actual username
        'password': 'xx'  # Replace with your actual password
    }
    response = requests.post(url, data=data)
    print(response.json())

# get_user_token()
