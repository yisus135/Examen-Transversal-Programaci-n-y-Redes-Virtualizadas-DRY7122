def es_as_privado(numero_as):
    if 64512 <= numero_as <= 65534:
        return True
    else:
        return False

def main():
    numero_as = input("Ingrese el número de AS de BGP: ")
    try:
        numero_as = int(numero_as)
        if es_as_privado(numero_as):
            print(f"El AS {numero_as} es privado.")
        else:
            print(f"El AS {numero_as} es público.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()