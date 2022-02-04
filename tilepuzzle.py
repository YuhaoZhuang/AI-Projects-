import copy
import heapq

# global list to keep track of visited state
repeated = []

# Priority queue class
class MyPriQueue(object):
    def __init__(self):
        self.heap = []
    # push to queue
    def add(self, key, value):
        heapq.heappush(self.heap, (value, key))
    # pop from queue
    def get(self):
        key, value = heapq.heappop(self.heap)
        return value

# main function, return expected output
def rushhour(state, currState):
    global repeated
    #repeated.append(currState)
    # save a copy of the original state
    original = currState
    # generated states
    states = []
    # library to keep track of previous state
    prev = {}
    # number of frontier states
    count = 0
    # queue to keep track of path 
    heap = MyPriQueue()

    # if states != goal, keep generating new states
    while check_final(currState) == False:
        generated = generateNewStates(currState)
        for each in generated:
            states.append(each)
        if states == []:
            repeated.clear()
            return []

        # update previous state library 
        for each in generated:
            prev[convert_to_string(each)] = convert_to_string(currState)

        # caculate heuristics f(n)
        state_value = {}
        for i in range(len(generated)):
            each = generated[i]
            # blocking state heuristic 
            if state == 0:
                value = heruristic_0(each) + path_length(prev, convert_to_string(each), convert_to_string(original))
            # own heuristic 
            if state == 1:
                value = heruristic_1(each) + path_length(prev, convert_to_string(each), convert_to_string(original))
            state_value[convert_to_string(each)] = value
        # push all generated states to heap 
        for each in state_value:
            heap.add(each, state_value[each])
        # pop lowest f(n) value state from heap
        currState = heap.get()   
        currState = convert(currState)
        count +=1
        # check for cycles
        while (currState in repeated):
            currState = heap.get()   
            currState = convert(currState)
        repeated.append(currState)

    # print path 
    li = convert_to_array(prev, convert_to_string(currState), convert_to_string(original))
    print_path(li)
    # empty global variable
    repeated.clear()
    print("Total moves:", len(li)-1 )
    print("Total states explored:", count)


# calculate how many cars/trucks are blocking in front of XX, take current state, return the total count
def block_count(currState):
    # get starting position of car X
    x_head = 0
    for i in range(5):
        if currState[2][i] == "X":
            x_head = i
            break
    count = 0
    # get # of cars/trucks blocking
    for i in range(x_head+2,5):
        if currState[2][i] != "-":
            count += 1
    return count

# heuristic 0, blocking heuristic, take current State, return h(n)
def heruristic_0(currState):
    count = block_count(currState)
    # plus one 
    if count >= 0:
        count += 1
    return count

# own heuristic, = how many cars blocking in front of XX + if those cars cannot be moved out of the way for XX to move, take current State, return h(n)
def heruristic_1(currState):
    # get starting position of car X
    x_head = 0
    for i in range(5):
        if currState[2][i] == "X":
            x_head = i
            break
    count = block_count(currState)
    length_car = 0
    for i in range(x_head+2,5):
        if currState[2][i] != "-":
            axis_li = get_vertical_axis(2, i, currState)
            head = axis_li[0]
            tail = axis_li[len(axis_li)-1]
            length_car = len(axis_li)
        # check to see if the cars blocking XX can be moved out of the way, if not, plus 1
        if length_car == 2:
            if not(currState[1][i] == "-" or currState[3][i] == "-"):
                count += 1
        elif length_car == 3:
            if currState[0][i] == head:
                if not(currState[3][i] == "-" and currState[4][i] == "-" and currState[5][i] == "-"):
                    count += 1
            elif currState[1][i] == head:
                if not(currState[4][i] == "-" and currState[5][i] == "-"):
                    count += 1
            elif currState[2][i] == head:
                if not(currState[5][i] == "-"):
                    count += 1
    return count

# check to see if car/truck is placed vertically, takes the x, y corrdinate, and the current State, return true if yes, false if no     
def check_vertical(x,y,currState):
    # if head of car/truck is at top of the puzzle
    if x == 0:
        if currState[x][y] == currState[x+1][y]:
            return True
    # if head of car/truck is at end of the puzzle
    elif x == 5:
        if currState[x][y] == currState[x-1][y]:
            return True
    # if neither head or tail of car/truck is placed at top or end of puzzle
    else :
        if currState[x][y] == currState[x-1][y]:
            return True
        elif currState[x][y] == currState[x+1][y]:
            return True
    return False

# return the list that contains head and tail of the car if it's vertical, take x, y coordinate of car, current State, return a list of all the x coordinates of the car
def get_vertical_axis(x,y,currState):
    # list to keep track of all the positions of the car
    li = []
    li.append(x)
    # check to see if head of car mathces those corrdinates
    if x == 0:
        if currState[x][y] == currState[x+1][y]:
            li.append(x+1)
        if currState[x][y] == currState[x+2][y]:
            li.append(x+2)
    elif x == 1:
        if currState[x][y] == currState[x-1][y]:
            li.append(x-1)
        if currState[x][y] == currState[x+1][y]:
            li.append(x+1)
        if currState[x][y] == currState[x+2][y]:
            li.append(x+2)
    elif x == 2 or x == 3:
        if currState[x][y] == currState[x-2][y]:
            li.append(x-2)
        if currState[x][y] == currState[x-1][y]:
            li.append(x-1)
        if currState[x][y] == currState[x+1][y]:
            li.append(x+1)
        if currState[x][y] == currState[x+2][y]:
            li.append(x+2)
    elif x == 4:
        if currState[x][y] == currState[x-2][y]:
            li.append(x-2)
        if currState[x][y] == currState[x-1][y]:
            li.append(x-1)
        if currState[x][y] == currState[x+1][y]:
            li.append(x+1)
    elif x == 5:
        if currState[x][y] == currState[x-2][y]:
            li.append(x-2)
        if currState[x][y] == currState[x-1][y]:
            li.append(x-1)
    # sort the list and return
    li.sort()
    return li

# return the list that contains head and tail of the car if it's horizontal, take x, y coordinate of car, current State, return a list of all the y coordinates of the car
def get_horizontal_axis(x,y,currState):
    # list to keep track of all the positions of the car
    li = []
    li.append(y)
    # check to see if head of car mathces those corrdinates
    if y == 0:
        if currState[x][y] == currState[x][y+1]:
            li.append(y+1)
        if currState[x][y] == currState[x][y+2]:
            li.append(y+2)
    elif y == 1:
        if currState[x][y] == currState[x][y-1]:
            li.append(y-1)
        if currState[x][y] == currState[x][y+1]:
            li.append(y+1)
        if currState[x][y] == currState[x][y+2]:
            li.append(y+2)
    elif y == 2 or y == 3:
        if currState[x][y] == currState[x][y-2]:
            li.append(y-2)
        if currState[x][y] == currState[x][y-1]:
            li.append(y-1)
        if currState[x][y] == currState[x][y+1]:
            li.append(y+1)
        if currState[x][y] == currState[x][y+2]:
            li.append(y+2)
    elif y == 4:
        if currState[x][y] == currState[x][y-2]:
            li.append(y-2)
        if currState[x][y] == currState[x][y-1]:
            li.append(y-1)
        if currState[x][y] == currState[x][y+1]:
            li.append(y+1)
    elif y == 5:
        if currState[x][y] == currState[x][y-2]:
            li.append(y-2)
        if currState[x][y] == currState[x][y-1]:
            li.append(y-1)
    # sort the list and return
    li.sort()
    return li


# slide the car up and return the new State. Take x1, x2, and y corrdinate of the card, current state, and return the new State
def slide_up(head,tail,y,currState):
    # generate copy of the current state
    newState = copy.deepcopy(currState)
    # check to see if car/truck can be slide up 
    if head != 0:
        if newState[head-1][y] == "-":
            car = newState[head][y]
            newState[tail] = currState[tail][:y] + "-" + currState[tail][y+1:]
            for i in range (head, tail+1):
                newState[i-1] = currState[i-1][:y] + car + currState[i-1][y+1:]
    return newState

# slide the car down and return the new State. Take x1, x2, and y corrdinate of the card, current state, and return the new State 
def slide_down(head,tail,y,currState):
    # generate copy of the current state
    newState = copy.deepcopy(currState)
    # check to see if car/truck can be slide down
    if tail != 5:
        if newState[tail+1][y] == "-":
            car = newState[head][y]
            newState[head] = currState[head][:y] + "-" + currState[head][y+1:]
            for i in range (head, tail+1):
                newState[i+1] = currState[i+1][:y] + car + currState[i+1][y+1:]
    return newState

# slide the car left and return the new State. Take x, y1, and y2 corrdinate of the card, current state, and return the new State 
def slide_left(head,tail,x,currState):
    # generate copy of the current state
    newState = copy.deepcopy(currState)
    newString = ''
    # check to see if car/truck can be slide left
    if head != 0:
        if newState[x][head-1] == "-":
            car = newState[x][head]
            for i in range(0,head-1):
                newString += currState[x][i]
            for i in range(head-1,tail):
                newString += car
            newString += "-"
            for i in range(tail+1,6):
                newString += currState[x][i]
            newState[x] = newString
    return newState

# slide the car right and return the new State. Take x, y1, and y2 corrdinate of the card, current state, and return the new State 
def slide_right(head,tail,x,currState):
    # generate copy of the current state
    newState = copy.deepcopy(currState)
    newString = ''
    # check to see if car/truck can be slide right
    if tail != 5:
        if newState[x][tail+1] == "-":
            car = newState[x][head]
            for i in range(0,head):
                newString += currState[x][i]
            newString += "-"
            for i in range(head+1,tail+2):
                newString += car
            for i in range(tail+2,6):
                newString += currState[x][i]
            newState[x] = newString
    return newState

# generate new states, take currentState, and return the list of states that are generated
def generateNewStates(currState):
    global repeated
    # list to keep track of generated states
    li = []
    # dictionary to keep track of visited cars/trucks
    keep = {}
    # generate new states
    for x in range(len(currState)):
        for y in range(len(currState[x])):
            if currState[x][y] != "-" and currState[x][y] not in keep:
                # if car/truck vertical
                if check_vertical(x,y,currState):
                    # get vertical axis
                    axis_li = get_vertical_axis(x, y, currState)
                    head = axis_li[0]
                    tail = axis_li[len(axis_li)-1]
                    # slide up 
                    newState = slide_up(head,tail,y,currState)
                    if newState not in repeated:
                        li.append(newState)
                    # slide down
                    newState = slide_down(head,tail,y,currState)
                    if newState not in repeated:
                        li.append(newState)
                    keep[currState[x][y]] = 1
                else:
                    # get horizontal axis
                    axis_li = get_horizontal_axis(x, y, currState)
                    head = axis_li[0]
                    tail = axis_li[len(axis_li)-1]
                    # slide left
                    newState = slide_left(head,tail,x,currState)
                    if newState not in repeated:
                        li.append(newState)
                    # slide right
                    newState = slide_right(head,tail,x,currState)
                    if newState not in repeated:
                        li.append(newState)
                    keep[currState[x][y]] = 1                    
    return li

# check to see if state is at the final position, take current state, return True if yes, False if no
def check_final(currState):
    if currState[2][4] == "X" and currState[2][5] == "X":
        return True
    return False

# calculate path lengh, take the dictionary containing the previous paths, current State, and original State, return how many states does it traversed from original State to current State
def path_length(dictionary, state, original):
    i = 0
    while(state != original):
        state = dictionary[state]
        i += 1
    return i

# convert 1 state from array to string , take current State, and returns a string of it 
def convert(currState):
    state = []
    i = 0
    j = 6
    for x in range(6):
        string = currState[i:j]
        state.append(string)
        i += 6
        j += 6
    return state

# convert multiple states from arrays to strings, take current State, and return a list of strings 
def convert_to_string(currState):
    string = ""
    for each in currState:
        string += each
    return string

# get the optimal path from dictionary, then reverse the array, take the dictionary that contains the previuos paths, current state, and original State, return the path from original State to current State 
def convert_to_array(dictionary, state, original):
    path = []
    path.append(state)
    while(state != original):
        state = dictionary[state]
        path.append(state)
    path.reverse()
    return path

# print the path , take the optimal path, and print it out in terminal
def print_path(path):
    for each in path:
        i = 0
        j = 6
        for x in range(6):
            print(each[i:j])
            i += 6
            j += 6
        print()
