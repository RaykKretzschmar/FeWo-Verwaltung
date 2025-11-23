import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fewo.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from customers.models import Customer

def run_security_test():
    print("Starting Security & Data Isolation Test...")

    # 1. Setup Users
    user1_name = "sec_test_user1"
    user2_name = "sec_test_user2"
    passw = "password123"

    # Clean up previous runs
    User.objects.filter(username__in=[user1_name, user2_name]).delete()

    user1 = User.objects.create_user(username=user1_name, password=passw)
    user2 = User.objects.create_user(username=user2_name, password=passw)
    print(f"Created test users: {user1_name}, {user2_name}")

    # 2. User 1 creates data
    client1 = Client()
    client1.login(username=user1_name, password=passw)
    
    # Create a customer for User 1
    response = client1.post('/customers/create/', {
        'first_name': 'User1',
        'last_name': 'Customer',
        'customer_type': 'Privat',
        'city': 'Berlin',
        'postal_code': '10115',
        'street': 'Teststr',
        'house_number': '1'
    })
    
    if response.status_code != 302:
        print(f"FAILED: User 1 could not create customer. Status: {response.status_code}")
        return

    user1_customer = Customer.objects.get(user=user1)
    print(f"User 1 created customer: {user1_customer} (ID: {user1_customer.id})")

    # 3. User 2 tries to see data
    client2 = Client()
    client2.login(username=user2_name, password=passw)

    # Test List View
    response = client2.get('/customers/')
    if user1_customer.first_name.encode() in response.content:
        print("FAILED: User 2 can see User 1's customer in list view!")
    else:
        print("PASSED: User 2 cannot see User 1's customer in list view.")

    # Test Direct Access (IDOR) - Update View
    response = client2.get(f'/customers/{user1_customer.id}/update/')
    if response.status_code == 404:
        print(f"PASSED: User 2 gets 404 when trying to update User 1's customer (IDOR protected).")
    elif response.status_code == 200:
        print(f"FAILED: User 2 can access update page for User 1's customer!")
    else:
        print(f"WARNING: Unexpected status code for update access: {response.status_code}")

    # Test Direct Access (IDOR) - Delete View
    response = client2.get(f'/customers/{user1_customer.id}/delete/')
    if response.status_code == 404:
        print(f"PASSED: User 2 gets 404 when trying to delete User 1's customer (IDOR protected).")
    elif response.status_code == 200:
        print(f"FAILED: User 2 can access delete page for User 1's customer!")
    else:
        print(f"WARNING: Unexpected status code for delete access: {response.status_code}")

    # Cleanup
    user1.delete()
    user2.delete()
    print("Test Users deleted.")
    print("Security Test Completed.")

if __name__ == "__main__":
    run_security_test()
