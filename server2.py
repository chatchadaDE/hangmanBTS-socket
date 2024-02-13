import socket
import random

def choose_word():
    words = ["numjoon", "seokjin", "yoongi", "hoseok", "jimin", "taehyung", "jungkook"]
    return random.choice(words)

def display_word(word, guessed_letters):
    return ''.join([letter if letter in guessed_letters else '_' for letter in word])

def run_server():
    host = '127.0.0.1'
    port = 12000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    word_to_guess = choose_word()
    guessed_letters = []
    attempts = 7

    if word_to_guess == 'numjoon': conn.send(f"who is the leader of BTS? \n Press enter for start game".encode())
    elif word_to_guess == 'seokjin': conn.send(f"who is the oldest member of BTS? \n Press enter for start game".encode())
    elif word_to_guess == 'yoongi': conn.send(f"which BTS member also goes by the stage name Agust-D? \n Press enter for start game".encode())
    elif word_to_guess == 'hoseok': conn.send(f"who is the sunshine of BTS? \n Press enter for start game".encode())
    elif word_to_guess == 'jimin': conn.send(f"who has ever studied poping and blocking dancing? \n Press enter for start game".encode())
    elif word_to_guess == 'taehyung': conn.send(f"who recived the 4D nickname? \n Press enter for start game".encode())
    elif word_to_guess == 'jungkook': conn.send(f"who is the maknae of BTS? \n Press enter for start game".encode())

    conn.send(f"HTTP/1.1 200 OK\r\n\r\nWelcome to Hangman! {display_word(word_to_guess, guessed_letters)} Attempts left: {attempts}".encode())

    
    
    while True:
        data = conn.recv(1024).decode()

        if not data:
            break

        if data.lower() in guessed_letters:
            conn.send("HTTP/1.1 400 Bad Request\r\n\r\nYou already guessed that letter. Try again.".encode())
        elif data.lower() in word_to_guess:
            guessed_letters.append(data.lower())
            current_display = display_word(word_to_guess, guessed_letters)
            if '_' not in current_display:
                conn.send(f"HTTP/1.1 200 OK\r\n\r\nCongratulations! You guessed the word: {word_to_guess}".encode())
                break
            else:
                conn.send(f"HTTP/1.1 200 OK\r\n\r\nCorrect! {current_display} Attempts left: {attempts}".encode())
        else:
            attempts -= 1 
            if attempts == 0:
                conn.send(f"HTTP/1.1 200 OK\r\n\r\nGame over! The word was: {word_to_guess}".encode())
                break
            conn.send(f"HTTP/1.1 200 OK\r\n\r\nWrong guess! {display_word(word_to_guess, guessed_letters)} Attempts left: {attempts}".encode())
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    run_server()
