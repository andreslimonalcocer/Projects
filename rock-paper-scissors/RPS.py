import random

def join(moves):
    return "".join(moves)

def player(prev_play, opponent_history=[], steps = {}):

    ideal_moves = {"R": "P", "P": "S", "S": "R"}

    if prev_play != "":
        opponent_history.append(prev_play)
    

    n = 5
    hist = opponent_history
    guess = random.choice(['R', 'P', 'S'])

    if len(hist) > n:
        pattern = join(hist[-n:])

        if join(hist[-(n + 1):]) in steps.keys():
            steps[join(hist[-(n + 1):])] += 1
        else:
            steps[join(hist[-(n + 1):])] = 1

        possible = [pattern + "R", pattern + "P", pattern + "S"]

        for i in possible:
            if not i in steps.keys():
                steps[i] = 0

        predict = max(possible, key = lambda key: steps[key])
        guess = ideal_moves[predict[-1]]

    return guess
