from collections import Counter

def numero_mas_frecuente(lista):

    conteo = Counter(lista)
    max_frecuencia = max(conteo.values())
    candidatos = [num for num, freq in conteo.items() if freq == max_frecuencia]
    return min(candidatos)

# Pruebas
if __name__ == "__main__":
    print(numero_mas_frecuente([1, 3, 1, 3, 2, 1]))  
    print(numero_mas_frecuente([4, 4, 5, 5]))        
    print(numero_mas_frecuente([7, 7, 8, 8, 9]))     
    print(numero_mas_frecuente([10]))               
    print(numero_mas_frecuente([3, 3, 2, 2, 1, 1]))  
