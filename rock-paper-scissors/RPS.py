# This bot successfuly defeats quincy, mrugesh and kris consistently with more than 60% of win rate, however it barely defeat
# abbey with that win rate, so if it fails try again so it defeat all bots with more than that win rate.

def player(prev_play, opponent_history = [], play_order = {}):

    # Import necessary libraries
    import heapq
    import random

    # Build ideal moves dictionary
    ideal_moves = {"R": "P", "P": "S", "S": "R"}

    # Build oppenent history, we ignore the first element of the list because it is always ""
    if prev_play != "":
        opponent_history.append(prev_play)

    # Define a window size to analyze opponents patterns
    window_size = 6

    # Analyze opponent patern when the history is larger than window size
    if len(opponent_history) > window_size:
        # Build opponent pattern
        pattern = "".join(opponent_history[-window_size:])
        # Update frequency opponent moves
        if "".join(opponent_history[-(window_size + 1):]) in play_order.keys():
            play_order["".join(opponent_history[-(window_size + 1):])] += 1
        else:
            play_order["".join(opponent_history[-(window_size + 1):])] = 1

        # Create a priority que for possible moves
        possible_moves = []
        for move in ['R', 'P', 'S']:
            freq = play_order.get(pattern + move, 0)
            # Insert element
            heapq.heappush(possible_moves, (-freq, move))

        # Extract element
        _, predict = heapq.heappop(possible_moves)
        # Chosse more probable move
        guess = ideal_moves[predict]

    else:
    # Generate random moves when needed
        guess = random.choice(['R', 'P', 'S'])

    return guess