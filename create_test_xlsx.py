import pandas as pd

def make_test_xlsx(filename):
    data = {
        'First Name': ['John', 'john', 'Jane', 'Jon'],
        'Last Name': ['Smith', 'Smith', 'Doe', 'Smith'],
        'Address': ['123 Main St', '123 main st', '456 Oak Ave', '123 Main St'],
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    make_test_xlsx("dedup_input.xlsx")
    make_test_xlsx("test_contacts.xlsx")
