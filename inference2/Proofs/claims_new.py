def pop_sent():
    sent = [
        [0, "it is|a consistent that there is|e a mind which is|a a|r dog and|c"],
        # [ 0,"It is|a consistent that there is|e a mind which is|a mental"],
        [1, "It is|a contradictory that there is|e a mind which is|a not mental"],
        [2, "It is|a consistent that no thought smells"],
        [3, "It is|a contradictory that there is|e a thought which smells"],
        [4, "It is|a contradictory that some|p thoughts smell"],
        [5, "It is|a contradictory that there is|e a mind which smells"],
        [6, "It is|a consistent that no mind smells"],
        [7, "It is|a contradictory that some|p minds smell"],
        [8, "It is|a consistent that no thought desires something"],
        [9, "It is|a contradictory that there is|e a thought which desires something"],
        [10, "It is|a contradictory that some|p thoughts desire something"],
        [11, "It is|a contradictory that no thought is|g a|r group"],
        [12, "It is|a consistent that there is|e a thought which is|g a|r group"],
        [13, "It is|a consistent that every thought is|a mental|b"],
        [14, "It is|a contradictory that there is|e a thought which is|a not mental|b"],
        [15, "It is|a contradictory that some|p thoughts are|a not mental"],
        [16, "It is|a contradictory that some|p thoughts are|g moments"],
        [17, "It is|a consistent that no thought thinks something"],
        [18, "It is|a contradictory that some|p thoughts think something"],
        [19, "It is|a contradictory that there is|e a thought which thinks something"],
        [20, "It is|a consistent that every mind is|a mental"],
        [21, "It is|a contradictory that no mind is|a mental"],
        [22, "It is|a contradictory that there is|e a thought which is|a physical"],
        [23, "It is|a consistent that there is|e a moment which exists in|b time"],
        [24, "It is|a contradictory that there is|e a moment which does not exist in|b time"],
        [25, "It is|a contradictory that there is|e a moment which is|a physical"],
        [26, "It is|a contradictory that there is|e a thought which is|g a|r moment"],
        [27, "It is|a consistent that no thought is|g a|r moment"],
        [28, "It is|a consistent that I do not have a point"],
        [29, "It is|a contradictory that I have a point"],
        [30, "It is|a contradictory that there is|e a point which smells"],
        [31, "It is|a contradictory that some|p points smell"],
        [32, "It is|a contradictory that there is|e a point which thinks some|p thoughts"],
        [33, "It is|a contradictory that some|p points think something"],
        [34, "It is|a contradictory that there is|e a point which is|a physical"],
        [35, "It is|a contradictory that some|p points are|a physical"],
        [36, "It is|a consistent that no whole|c is|g an|r individual"],
        [37, "It is|a contradictory that there is|e a whole|c which is|g an|r individual"],
        [38, "It is|a consistent that there is|e a whole which is|g not an|r individual"],
        [39, "It is|a consistent that there is|e a whole which is|g an|r individual"],
        [40, "It is|a consistent that JFK is|g a|r Kennedy and JFK is|g part|f of the|r family Kennedy"],
        [41, "It is|a contradictory that JFK is|g a|r Kennedy and JFK is|g not part|f of the|r family Kennedy"],
        [42, "It is|a contradictory that JFK is|g not a|r Kennedy and JFK is|g part|f of the|r family Kennedy"],
        [43, "It is|a contradictory that JFK is|g a|r Kennedy and JFK is|g not part|f of the|r family Kennedy"],
        [44, "It is|a consistent that dog is|g a|r class"],
        [45, "It is|a contradictory that dog is|g not a|r class"],
        [46, "It is|a consistent that a universal is|r distinct from its|a instance"],
        [47, "It is|a contradictory that a universal is|r not distinct from its|a instance"],
        [48, "It is|a consistent that there is|e a universal which is|r distinct from its|a instances"],
        [49, "It is|a contradictory that there is|e a universal which is|r not distinct from its|a instances"],
        [50, "It is|a consistent that the|r concept|n dog is|g not a|r dog"],
        [51, "It is|a contradictory that the|r concept|n dog is|g itself|r a|r dog"],
        [52, "It is|a consistent that dog is|g a|r concept|n"],
        [53, "It is|a contradictory that dog is|g not a|r concept|n"],
        [54, "It is|a consistent that point is|g not a|r partially material|a concept|n"],
        [55, "It is|a contradictory that point is|g a|r partially material|a concept|n"],
        [56, "It is|a consistent that this dog is|g not a|r concept|n"],
        [57, "It is|a contradictory that this dog is|g a|r concept|n"],
        [58, "It is|a consistent that thought is|g not a|r partially material|a concept|n"],
        [59, "It is|a contradictory that thought is|g a|r partially material|a concept|n"],
        [60, "It is|a consistent that Russell is|g a|r man"],
        [61, "It is|a contradictory that Russell is|g not a|r man"],
        [62, "It is|a consistent that this cat is|g a|r cat"],
        [63, "It is|a contradictory that this cat is|g not a|r cat"],
        [64, "It is|a contradictory that I desire a concept|n"],
        [65, "It is|a consistent that I do not desire a concept|n"],
        [66, "It is|a contradictory that there is|e a concept|n which is|g an|r individual|a thing"],
        [67, "It is|a consistent that no concept|n is|g an|r individual|a thing"],
        [68, "It is|a contradictory that this|n is|g a|r particular dog and this|n is the|r concept|n dog"],
        [69, "It is|a consistent that this|n is|g a|r particular dog and this|n is not the|r concept|n dog"],
        [70, "It is|a contradictory that redness is|g not a|r particular concept|b and this|n has redness"],
        [71, "It is|a consistent that redness is|g a|r particular concept|b and this|n has redness"],
        [72, "It is|a contradictory that this particular man has|m some|p instances"],
        [73, "It is|a consistent that this particular man does not have|m some|p instances"],
        [74, "It is|a contradictory that this particular woman is|g not an|r instance|i of the|r concept|n woman"],
        [75, "It is|a consistent that this particular woman is|g an|r instance|i of the|r concept|n woman"],
        [76, "It is|a consistent that the|r concept|n mind is|r not in|r this house"],
        [77, "It is|a contradictory that the|r concept|n mind is|r in|r this house"],
        [78, "It is|a contradictory that I ate an apple and apple is|g not an|r abstract|t term"],
        [79, "It is|a consistent that I ate an apple and apple is|g an|r abstract|t term"],
        [80, "It is|a consistent that every number|i does not smell"],
        [81, "It is|a contradictory that there is|e a number|i which smells"],
        [82, "It is|a contradictory that some|p numbers|i smell"],
        [83, "It is|a contradictory that there is|e a number|i which is|a physical"],
        [84, "It is|a contradictory that some|p numbers|i are|a physical"],
        [85, "It is|a contradictory that Julius Caesar is|g a|r number|i"],
        [86, "It is|a consistent that Julius Caesar is|g not a|r number|i"],
        [87, "It is|a contradictory that a moment is|r greater than a number|i"],
        [88, "It is|a consistent that a moment is|r not greater than a number|i"],
        [89, "It is|a consistent that the|r property|n redness is|a not red"],
        [90, "It is|a contradictory that the|r property|n redness is|a red"],
        [91,
         "It is|a consistent that Russell has|c|r the|r causal role 'can hit' and the|r causal role 'can hit' is|g a|r property|n"],
        [92,
         "It is|a contradictory that Russell has|c|r the|r causal role can hit and the|r causal role can hit is|g not a|r property|n"],
        [93, "It is|a contradictory that there is|e a property which is|g an individual"],
        [94, "It is|a consistent that no property|n is|g an individual"],
        [95, "It is|a contradictory that the|r property|n redness is|r composed of some|p particles"],
        [96, "It is|a consistent that the|r property|n redness is|r not composed of some|p particles"],
        [97, "It is|a consistent that Plato has|t the same teacher as Xenothon and Xenothon has|t a teacher"],
        [98,
         "It is|a contradictory that Plato has|t the same teacher as Xenothon and Xenothon does not have|t a teacher"],
        [99,
         "It is|a consistent that Plato has|t the same teacher as Xenothon and that|d teacher is Socrates and Socrates teaches Xenothon"],
        [100,
         "It is|a contradictory that Plato has|t the same teacher as Xenothon and that|d teacher is Socrates and Socrates does not teach Xenothon"],
        [101,
         "It is|a consistent that I saw the same movie as you and that|d movie was Casablanca and I saw Casablanca"],
        [102,
         "It is|a contradictory that I saw the same movie as you and that|d movie was Casablanca and I did not see Casablanca"],
        [103,
         "It is|a consistent that Leibniz and|c Aristotle ate from the same cake and this|n was that|d cake and Leibniz ate from this|n"],
        [104,
         "It is|a contradictory that Leibniz and|c Aristotle ate from the same cake and this|n was that|d cake and Leibniz did not eat from this|n"],
        [105,
         "It is|a consistent that every part|p of the large house is|a white and the door is|g a|r part|p of the large house and the door is|a white"],
        [106,
         "It is|a contradictory that every part|p of the large house is|a white and the door is|g a|r part|p of the large house and the door is|a not white"],
        [107,
         "It is|a contradictory that no part|p of the large house is|a white and the door is|g a|r part|p of the large house and the door is|a white"],
        [108,
         "It is|a consistent that I saw everyone who drank something in|m the van and Leibniz drank something in|m the van and I saw Leibniz"],
        [109,
         "It is|a contradictory that I saw everyone who drank something in|m the van and Leibniz drank something in|m the van and I did not see Leibniz"],
        [110,
         "It is|a consistent that I love nothing which is|r about murder and Hamlet is|r about murder and I do not love Hamlet"],
        [111,
         "It is|a contradictory that I love nothing which is|r about murder and hamlet is|r about murder and I love Hamlet"],
        [112,
         "It is|a consistent that I love anything which is|r about logic and set theory is|r about logic and I love set theory"],
        [113,
         "It is|a contradictory that I love anything which is|r about logic and set theory is|r about logic and I do not love set theory"],
        [114,
         "It is|a consistent that no green man from|b cold Mars, lives on|r Earth and Jim is|g a|r green man born|p on|r Mars and Jim does not live on|r Earth"],
        [115,
         "It is|a contradictory that no green man from|b cold Mars, lives on|r Earth and Jim is|g a|r green man born|p on|r Mars and Jim lives on|r Earth"],
        [116,
         "It is|a consistent that every green man from|b Mars drinks and Jim is|g a|r green man born|p on|r Mars and Jim drinks"],
        [117,
         "It is|a contradictory that every green man from|b Mars drinks and Jim is|g a|r green man born|p on|r Mars and Jim does not drink"],
        [118,
         "It is|a consistent that everyone who spies on Leibniz, will|r be|a rewarded and Russell spied on Leibniz and Russell was|a rewarded"],
        [119,
         "It is|a contradictory that everyone who spies on Leibniz, will|r be|a rewarded and Russell spied on Leibniz and Russell was|a not rewarded"],
        [120,
         "It is|a consistent that everyone who spies on a nazi in|m Munich, will|r be|a rewarded and Russell spied on a nazi in|m Munich and Russell was|a rewarded"],
        [121,
         "It is|a contradictory that everyone who spies on a nazi in|m Munich, will|r be|a rewarded and Russell spied on a nazi in|m Munich and Russell was|a not rewarded"],
        [122,
         "It is|a consistent that anyone who breaks the speed limit, will|r be|a caught and Marilyn broke the speed limit and Marilyn was|a caught"],
        [123,
         "It is|a contradictory that anyone who breaks the speed limit, will|r be|a caught and Marilyn broke the speed limit and Marilyn was|a not caught"],
        [124, "It is|a consistent that I did not shed a tear and I did not shed some|p tears"],
        [125, "It is|a contradictory that I did not shed a tear and I shed some|p tears"],
        [126,
         "It is|a consistent that every woman at|c the party drank and Jessica was|r at|c the party and Jessica is|g a|r woman and Jessica drank"],
        [127,
         "It is|a contradictory that every woman at|c the party drank and Jessica was|r at|c the party and Jessica is|g a|r woman and Jessica did not drink"],
        [128,
         "It is|a consistent that every woman at|c the party drank and Jessica was|g a|r woman at|c the party and Jessica drank"],
        [129,
         "It is|a contradictory that every woman at|c the party drank and Jessica was|g a|r woman at|c the party and Jessica did not drink"],
        [130,
         "It is|a consistent that no part|p of the large house is|a white and the door is|g a|r part|p of the large house and the door is|a not white"],
        [131, "It is|a consistent that I love everyone who reads Leibniz and Russell reads Leibniz and I love Russell"],
        [132,
         "It is|a contradictory that I love everyone who reads Leibniz and Russell reads Leibniz and I do not love Russell"],
        [133, "It is|a consistent that I did not shed any|n tears and I shed no tears"],
        [134, "It is|a contradictory that I did not shed any|n tears and I shed a tear"],
        [135, "It is|a consistent that my dog drank some water and I own a dog"],
        [136, "It is|a contradictory that my dog drank some water and I do not own a dog"],
        [137, "It is|a consistent that I saw my dog and I own a dog"],
        [138, "It is|a contradictory that I saw my dog and I do not own a dog"],
        [139, "It is|a consistent that I saw your dog and you do own a dog"],
        [140, "It is|a contradictory that I saw your dog and you do not own a dog"],
        [141, "It is|a consistent that your dog drank some water and you do own a dog"],
        [142, "It is|a contradictory that your dog drank some water and you do not own a dog"],
        [143, "It is|a consistent that I saw his dog and he owns a dog"],
        [144, "It is|a contradictory that I saw his dog and he does not own a dog"],
        [145, "It is|a consistent that his dog drank some water and he owns a dog"],
        [146, "It is|a contradictory that his dog drank some water and he does not own a dog"],
        [147, "It is|a consistent that I took the dog's ball and the dog owns a ball"],
        [148, "It is|a contradictory that I took the dog's ball and the dog does not own a ball"],
        [149, "It is|a consistent that the dog's ball is|a red and the dog owns a ball"],
        [150, "It is|a contradictory that the dog's ball is|a red and the dog does not own a ball"],
        [151, "It is|a consistent that Ada's ball is|a red and Ada owns a ball"],
        [152, "It is|a contradictory that Ada's ball is|a red and Ada does not own a ball"],
        [153, "It is|a consistent that I took Ada's ball and Ada owns a ball"],
        [154, "It is|a contradictory that I took Ada's ball and Ada does not own a ball"],
        [155, "It is|a consistent that I took a dog's ball and there is|e a dog which owns a ball"],
        [156, "It is|a contradictory that I took a dog's ball and no dog owns a ball"],
        [157, "It is|a consistent that Leibniz and|c Aristotle studied logic and Leibniz studied logic"],
        [158, "It is|a contradictory that Leibniz and|c Aristotle studied logic and Leibniz did not study logic"],
        [159, "It is|a consistent that Russell has the|r property|n courage and Russell is|a courageous"],
        [160, "It is|a contradictory that Russell has the|r property|n courage and Russell is|a not courageous"],
        [161, "It is|a consistent that Russell has courage and Russell is|a courageous"],
        [162, "It is|a contradictory that Russell has courage and Russell is|a not courageous"],
        [163, "It is|a contradictory that the door is|a not large and the door which is|a green is|a large"],
        [164, "It is|a consistent that this door is|a not large and this door which is|a green is|a not large"],
        [165, "It is|a contradictory that I did not shed a tear and I did not shed many|n tears"],
        [166, "It is|a consistent that I shed a tear and I shed many|n tears"],
        [167, "It is|a contradictory that many|n minds smell"],
        [168, "It is|a contradictory that many|n points smell"],
        [169, "It is|a contradictory that many|n numbers|i are|a physical"],
        [170, "It is|a contradictory that many|n points think something"],
        [171, "It is|a contradictory that many|n points are|a mental"],
        [172, "It is|a contradictory that many|n points are|a physical"],
        [173, "It is|a contradictory that few numbers|i smell"],
        [174, "It is|a contradictory that few thoughts are|a not mental"],
        [175, "It is|a contradictory that I have few points"],
        [176, "It is|a contradictory that I do not have many|n points"],
        [177, "It is|a contradictory that I ate an apple and apple is|g not a|r general|t term"],
        [178, "It is|a consistent that I ate an apple and apple is|g a|r general|t term"],
        [179, "It is|a contradictory that something exists inside of|r a point"],
        [180, "It is|a contradictory that no point exists within a region|a"],
        [181, "It is|a contradictory that this|n is|g a|r group of|i points and no points belong to this|n"],
        [182, "It is|a contradictory that there is|e a point which smells"],
        [183, "It is|a consistent that nothing exists inside of|r a point"],
        [184, "It is|a consistent that a point exists within a region|a"],
        [185, "It is|a consistent that this|n is|g a|r group of|i points and a point belong to this|n"],
        [186, "It is|a consistent that no point smells"],
        [187, "It is|a consistent that no thought is|a physical"],
        [188, "It is|a consistent that no moment is|a physical"],
        [189, "It is|a consistent that every point is|a not physical"],
        [190, "It is|a consistent that no number|i is|a physical"],
        [191, "It is|a contradictory that there is|a a thought which is|a physical"],
        [192, "It is|a contradictory that there is|e a moment which is|a physical"],
        [193, "It is|a contradictory that every point is|a physical"],
        [194, "It is|a contradictory that Plato is|g not an|r individual"],
        [195, "It is|a consistent that Plato is|g an|r individual"],
        [196, "It is|a consistent that Kiera Knightley is|g not an|r concept|n"],
        [197, "It is|a contradictory that Kiera Knightley is|g an|r concept|n"]]
    # [ 194,"It is|a contradictory that there is|a a number|i which is|a physical"],
    # [ 195,"It is|a contradictory that this wrinkle in that|d carpet is|g not an|r individual|a thing"],
    # [ 196,"It is|a consistent that this wrinkle in that|d carpet is|g an|r individual|a thing"],
    # [ 197,"It is|a consistent that a number|i is|a a|r universal"],
    # [ 198,"It is|a contradictory that a number|i is|a not a|r universal"],
    # [ 199,"It is|a contradictory that a universal is|a wholly present in space"],
    # [ 200,"It is|a consistent that no universal is|a wholly present in space"],
    # [ 201,"It is|a consistent that a set of particles has the quality 'being a man'"],
    # [ 202,"It is|a consistent that a set of particles does not have the quality 'being a man'"],
    # [ 203,"It is|a consistent that a particular is|g something that|r instantiates"],
    # [ 204,"It is|a contradictory that a particular is|g something that|r does not instantiate"],
    # [ 205,"It is|a consistent that a particular is|r not itself|r instantiated"],
    # [ 206,"It is|a contradictory that a particular is|r instantiated"],
    # [ 207,"It is|a consistent that a universal has|m an|r instance"],
    # [ 208,"It is|a contradictory that a universal does not have|m an|r instance"],
    # [ 209,"It is|a consistent that this apple is|a real|p and this apple is|a imaginary to Leibniz"],
    # [ 210,"It is|a contradictory that this apple is|a not real|p and this apple is|a imaginary to Leibniz"],
    # [ 211,"It is|a contradictory that this apple is|a real|p and this apple is|a fictional to Leibniz"],
    # [ 212,"It is|a consistent that this apple is|a not real|p and this apple is|a fictional to Leibniz"],
    # [ 213,"It is|a contradictory that this apple is|a fictional to Aristotle and this apple is|a imaginary to Aristotle"],
    # [ 214,"It is|a consistent that this apple is|a not fictional to Aristotle and this apple is|a imaginary to Aristotle"]]
    return sent, 500
