def perceptron(threshold, adjustment, weights, examples, passes):
    print("Starting weights:", weights)
    print("Threshold:", threshold, "Adjustment:", adjustment)
    # iterate through the number passes
    for pass_num in range(passes):
        print("")
        print("Pass", pass_num+1)
        print("")
        # iterate through the examples
        for each_ex in examples:
            total = 0
            # for each examples
            inputs = each_ex[1]
            for i in range(len(weights)):
                # calculate the total weight
                total += weights[i] * inputs[i]
            # check if the total weight is larger than the threshold or not
            prediction = True
            if total > threshold:
                prediction = True
            else:
                prediction = False
            # predicted False, correct answer True
            if total < threshold and each_ex[0] == True:
                for i in range(len(inputs)):
                    if inputs[i] == 1:
                        # adjust the weight by adding adjustment to it
                        weights[i] += adjustment
            # predicted True, correct answer False 
            if total > threshold and each_ex[0] == False:
                for i in range(len(inputs)):
                    if inputs[i] == 1:
                        # adjust the weight by subtracting adjustment to it
                        weights[i] -= adjustment

            print("inputs:", inputs)
            print("prediction:", prediction, "answer:", each_ex[0])
            print("adjusted weights:", weights)
                
