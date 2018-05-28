from socket import *
import socket
import json

def main():
    s = socket.socket(AF_INET, SOCK_STREAM)
    port = 8888
    host = socket.gethostname()
    s.bind((host, port))

    s.listen()
    while True:
        c, addr = s.accept()
        lista = get_notes_data('lista.json')

        print ('Got connection from', addr)
        c.send('Choose 1 option form list: \n1 - Wyswietl liste zadan \n2 - Dodaj zadanie(podaj najpierw opis, potem priorytet) \n3 - Usun zadanie(Podaj id) \n4 - Wyswietl liste zadan o danym priorytecie'.encode())
        opcja = bytes(c.recv(1234)).decode()
        if opcja == '1':
            notes = ""
            for note in lista:
                notes += str(note)
                notes += '\n'
            c.send(notes.encode())
        elif opcja == '2':
            text = bytes(c.recv(1234)).decode()
            priority = bytes(c.recv(1234)).decode()
            add_note(priority, text, lista)
            save_notes('lista.json', lista)
        elif opcja == '3':
            id = bytes(c.recv(1234)).decode()
            remove_note(id, lista)
            c.send("Usunieto element na podanej pozycji".encode())
        elif opcja == '4':
            priority = bytes(c.recv(1234)).decode()
            tmp = print_column(priority, lista)
            c.send(tmp.encode())
        else:
            c.send("Podano zla wartosc, wybierz co chcesz zrobic jeszcze raz".encode())
        c.close()

def get_notes_data(filename):
    with open(filename, 'r') as file_data:
        return json.loads(file_data.read())

def generate_id():
    max_id = 0
    for note in get_notes_data('lista.json'):
        if note['id'] > max_id:
            max_id = note['id']

    return max_id + 1

def save_notes(filename, notes):
    with open(filename, 'w') as notes_file:
        json.dump(notes, notes_file)

def add_note(priority, text, notes):
    note_data = {
            'id': generate_id(),
            'text': text,
            'priority': priority,
        }
    notes.append(note_data)
    save_notes('lista.json', notes)

def remove_note(note_id, notes):
    for note in notes:
        if note["id"] == note_id:
            notes.pop(notes.index(note))
    save_notes('lista.json', notes)

def print_column(priority, notes):
    tmp = ""
    for note in notes:
        if note['priority'] == priority:
            tmp += str(note)
            tmp += '\n'
    return tmp

if __name__ == "__main__":
    main()
