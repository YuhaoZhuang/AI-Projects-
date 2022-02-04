# take the board, size of board, color of the player, and how deep it searches. Then starts searching.  
def hexapawn(board, num, color, level):
    # convert board to a string
    currState = convert_to_string(board)
    if color == "w":
        start = 0
    else:
        start = 1
    # check if board is already won 
    if check_win(currState, num, "w") or check_win(currState, num, "b"):
        final_string = final(currState, num)
        print(final_string)
    # starts recursion
    recurse(currState, num, color, 0, level, start)

# minimax algorithm, take the currState, color of the player, current depth search, max depth of search, and the starting color of the player
# generates new States, evaluate using minimax algorithm, and return output 
def recurse(currState, num, color, curr_level, max_level, start):
    # if the board is won, return board evaluation
    if check_win(currState, num, color):
        return(evaluate(currState, num, color, start))
    # if maximum # of depth is reached, return board evaluation 
    if curr_level == max_level:
        return evaluate(currState, num, color, start)
    # generate new states
    li = generateNewStates(currState, num, color)
    num_list = []
    # for every new state, keep searching, all values is kept in a list for later min/max
    for each in li:
        if color =="w":
            num_list.append(recurse(each, num, "b", curr_level+1, max_level, start))
        else:
            num_list.append(recurse(each, num, "w", curr_level+1, max_level, start))
    # return maximum/minimum of the states based on the current dept of seasrch.
    # Since minimax always start with max first, then min... If current depth is even, return max, if current depth is odd, return min
    if curr_level > 0:
        if curr_level % 2 == 0:
            return max(num_list)
        else:
            return min(num_list)
    else:
        # return final answer
        if curr_level % 2 == 0:
            number = max(num_list)
            for i in range(len(num_list)):
                if number == num_list[i]:
                     final_string = final(li[i], num)
                     print(final_string)
                     break
        else:
            number = min(num_list)
            for i in range(len(num_list)):
                if number == num_list[i]:
                    final_string = final(li[i], num)
                    print(final_string)
                    break

# take the current State, num, and pawn position, check to see if the pawn can be moved downwards and return the new State
def move_down(currState, num, i):
    newString = ''
    y = i + num
    if y <num*num:
        if currState[y] == "-":
            newString += currState[:i]
            newString += "-"
            newString += currState[i+1:y]
            newString += currState[i]
            newString += currState[y+1:]
    return newString

# take the current State, num, and pawn position, check to see if the pawn can be moved upwards and return the new State
def move_up(currState, num, i):
    newString = ''
    y = i - num
    if y >= 0 :
        if currState[y] == "-":
            newString += currState[:y]
            newString += currState[i]
            newString += currState[y+1:i]
            newString += "-"
            newString += currState[i+1:]
    return newString

# take the current State, num, and pawn position, check to see if the pawn can be eat the opponent pawn to its top left and return the new State
def diagonal_left_up(currState, num, i):
    newString = ''
    if (i % num) > 0 :
        y = i -num - 1
        if y >= 0:
            if currState[y] == "w":
                newString += currState[:y]
                newString += currState[i]
                newString += currState[y+1:i]
                newString += "-"
                newString += currState[i+1:]
    return newString

# take the current State, num, and pawn position, check to see if the pawn can be eat the opponent pawn to its top right and return the new State
def diagonal_right_up(currState, num, i):
    newString = ''
    if (i % num) < num-1 :
        y = i -num + 1
        if y >= 0:
            if currState[y] == "w":
                newString += currState[:y]
                newString += currState[i]
                newString += currState[y+1:i]
                newString += "-"
                newString += currState[i+1:]
    return newString

# take the current State, num, and pawn position, check to see if the pawn can be eat the opponent pawn to its bottom left and return the new State
def diagonal_left_down(currState, num, i):
    newString = ''
    if (i % num) > 0 :
        y = i+num - 1
        if y < num*num:
            if currState[y] == "b":
                newString += currState[:i]
                newString += "-"
                newString += currState[i+1:y]
                newString += currState[i]
                newString += currState[y+1:]
    return newString

# take the current State, num, and pawn position, check to see if the pawn can be eat the opponent pawn to its bottom right and return the new State
def diagonal_right_down(currState, num, i):
    newString = ''
    if (i % num) < num-1:
        y = i + num + 1
        if y < num*num:
            if currState[y] == "b":
                newString += currState[:i]
                newString += "-"
                newString += currState[i+1:y]
                newString += currState[i]
                newString += currState[y+1:]
    return newString

# take current State, num, and color of the player, generate all possible new States and return them in a list
def generateNewStates(currState, num, color):
    li = []
    for i in range(num*num):
        # if color is white, try move down, eat bottom left, eat bottom right
        if color == "w":
            if currState[i] == "w":
                string = move_down(currState, num, i)
                if string != "":
                    li.append(string)
                string = diagonal_left_down(currState, num, i)
                if string != "":
                    li.append(string)
                
                string = diagonal_right_down(currState, num, i)
                if string != "":
                    li.append(string)     
        else:
            # if color is black, try move up, eat top left, eat top right
            if currState[i] == "b":
                string = move_up(currState, num, i)
                if string != "" and (string not in li):
                    li.append(string)
                string = diagonal_left_up(currState,num,i)
                if string != "" :
                    li.append(string)
                string = diagonal_right_up(currState,num,i)
                if string != "":
                    li.append(string)
    return li

# take current state, size of board, player color, and check to see if the board is stuck moving by trying to generate new states, True if board is stuck, False otherwise
def check_stuck(currState, num, color):
    # try to generate new States, check if list is empty
    li = generateNewStates(currState, num, color)
    if li == []:
        return True
    else:
        return False
# take current state, size of board, player color, and check to see if board has no more pawns of that color, return True if yes, false otherwise
def check_no_pawn(currState, num, color):
    # count how many pawns of player color does the board contain
    count = 0
    for i in currState:
        if i == color:
            count += 1
    if count > 0:
        return False
    else:
        return True

# take current state, size of board, player color, and check to see if one of the player's pawns has already reached at the end of the board, True if yes, false otherwise
def check_reach_end(currState, num, color):
    # search through the bottom of the board to see if there's any white pawns 
    if color == "w":
        for i in range(num*(num-1),num*num):
            if currState[i] == "w":
                return True
        return False
    # search through the bottom of the board to see if there's any black pawns 
    if color == "b":
        for i in range(num):
            if currState[i] == "b":
                return True
        return False 

# take current state, size of board, player color, and check to see if one of the opponent player has won already, True if yes, false otherwise
def check_win(currState, num, color):
    # see if the player gets stuck
    stuck = check_stuck(currState, num, color)
    # seee if the player has no pawns
    no_pawn = check_no_pawn(currState, num, color)
    # see if the opponent has reached the end 
    if color == "w":
        reach_end = check_reach_end(currState, num, "b")
    else:
        reach_end = check_reach_end(currState, num, "w")
    
    if stuck or no_pawn or reach_end:
        return True
    else:
        return False

# take current State, starting color of board, and return the score (professor's heuristic in class)
def calculate_score(currState, start):
    # count number of white pawns and black pawns on the board
    count_w = 0
    count_b = 0
    for each in currState:
        if each == "w":
            count_w += 1
        elif each == "b":
            count_b += 1
    # if board is white, return number of white pawns - number of black pawns
    if start == 0:
        total = count_w - count_b
    # if board is black, return number of black pawns - number of white pawns
    else:
        total = count_b - count_w
    return total

# take current State, player color of board, starting color of the board, and return the score 
def evaluate(currState, num, color, start):
    # if the board is won
    if check_win(currState, num, color):
        if color == "b" and start == 0:
            return num*num+1
        elif color == "w" and start == 0:
            return 0 - (num*num+1)
        elif color == "b" and start == 1:
            return 0 - (num*num+1)
        elif color == "w" and start == 1:
            return num*num+1
    else:
        return calculate_score(currState, start)
    
# take the board and return the currState into a string
def convert_to_string(currState):
    string = ""
    # append the strings
    for each in currState:
        string += each
    return string

# take the current State, size of board, and convert the string into final output 
def final(currState, num):
    i = 0
    y = num
    li = []
    # append the string to a list
    for a in range(num):
        li.append(currState[i:y])
        i += num
        y += num
    return li
