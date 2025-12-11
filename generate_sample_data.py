import csv

employees = [
    {"id":"1","name":"Alice","age":"30","department":"Engineering","salary":"70000"},
    {"id":"2","name":"Bob","age":"25","department":"Marketing","salary":"48000"},
    {"id":"3","name":"Carol","age":"28","department":"Engineering","salary":"65000"},
    {"id":"4","name":"Dan","age":"22","department":"Intern","salary":"24000"},
    {"id":"5","name":"Emma","age":"45","department":"HR","salary":"90000"},
]

products = [
    {"product_id":"1001","name":"Widget","price":"9.99","stock":"100"},
    {"product_id":"1002","name":"Gadget","price":"19.50","stock":"50"},
    {"product_id":"1003","name":"Thingy","price":"2.50","stock":"300"},
    {"product_id":"1004","name":"Doohickey","price":"15.00","stock":"0"},
]

def write_csv(path, rows):
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    write_csv("employees.csv", employees)
    write_csv("products.csv", products)
    print("Generated employees.csv and products.csv")
