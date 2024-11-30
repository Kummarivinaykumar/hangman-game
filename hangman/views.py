import random
from django.shortcuts import render, redirect

# List of words for the game
words = ['python', 'hangman', 'computer', 'programming', 'developer', 'software', 'algorithm', 'debugging', 'machine', 'learning']

def start_game(request):
    if 'word' not in request.session:
        request.session['word'] = random.choice(words)
        request.session['guessed_letters'] = ''
        request.session['tries'] = 0

    word = request.session['word']
    guessed_letters = request.session['guessed_letters']
    tries = request.session['tries']
    max_tries = 6

    if request.method == 'POST':
        guess = request.POST.get('guess', '').lower()
        if len(guess) == 1 and guess.isalpha() and guess not in guessed_letters:
            guessed_letters += guess
            request.session['guessed_letters'] = guessed_letters

            if guess not in word:
                tries += 1
                request.session['tries'] = tries

            if all(letter in guessed_letters for letter in word):
                return render(request, 'hangman/win.html', {'word': word})

            if tries >= max_tries:
                return render(request, 'hangman/lose.html', {'word': word})

    display_word = ''.join([letter if letter in guessed_letters else '_' for letter in word])
    request.session.modified = True  # Ensure the session is saved
    return render(request, 'hangman/game.html', {
        'display_word': display_word,
        'guessed_letters': sorted(guessed_letters),
        'tries_left': max_tries - tries,
    })

def reset_game(request):
    request.session.flush()  # Clear the session
    return redirect('start_game')