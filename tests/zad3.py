from tasks.zad3 import PasswordGenerator

def test_zad_3():
    password_gen = PasswordGenerator()
    print("\n===== Passwords =====")
    for i, password in enumerate(password_gen):
        print(f"{i}) {password}")
        
if __name__ == "__main__":
    test_zad_3()
        