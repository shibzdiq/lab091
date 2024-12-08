from urllib.parse import quote_plus

username = "shibzdik"
password = "shibZdik/\\123"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

print(f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.mongodb.net/car_catalog?retryWrites=true&w=majority")
