import concurrent.futures
import time
import requests

# Funkcja symulująca próbę logowania
def login_attempt(username, password):
    url = ""  # Adres URL do strony logowania
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(url, data=login_data)
        # Debugowanie odpowiedzi serwera
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text[:500]}")  # Wyświetl pierwsze 500 znaków odpowiedzi
        
        # Sprawdź, czy logowanie było udane
        if "Login successful" in response.text:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

# Funkcja do testowania wydajności
def performance_test(num_attempts, time_limit):
    username = ""
    password = ""
    
    start_time = time.time()
    successful_logins = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(login_attempt, username, password) for _ in range(num_attempts)]
        
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                successful_logins += 1
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Liczba prób logowania: {num_attempts}")
    print(f"Liczba udanych logowań: {successful_logins}")
    print(f"Całkowity czas: {elapsed_time:.2f} sekund")
    
    if elapsed_time <= time_limit and successful_logins >= num_attempts:
        print("Test zdany!")
    else:
        print("Test niezdany!")

# Testowanie wydajności dla 1000 logowań w 60 sekund
performance_test(1000, 60)
