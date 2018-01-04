import numpy as np

#0
#
#1  2
#3  4
#
# 5  6  7
# 8  9  10
# 11 12 13
#
# 14 15 16 17
# 18 19 20 21
# 22 23 24 25
# 26 27 28 29

class classGame(object):

    def __init__(self):
        patro0 = [0]
        patro1 = list(range(1,5))
        patro2 = list(range(5,14))
        patro3 = list(range(14,30))

        self.patra = [patro0,patro1,patro2,patro3]
        self.sides = [1,2,3,4]

    ## VISUALIZATION and BOARD HANDLING ##########################################

    def showTrinaryBoard(self,pole,patra = [[0],list(range(1,5)),list(range(5,14)),list(range(14,30))],sides = [1,2,3,4]):
        for p,a in enumerate(self.sides):
            patro = self.patra[p]
            values = pole[patro]
            #print(values)
            for y in range(a):
                x1 = y*a
                x2 = (y+1)*a
                values_row = values[x1:x2]
                print(values_row)

    def trinaryToBinaryBoard(self,pole_trinary):
        p = np.array(pole_trinary)
        ones = (p == 1)
        twos = (p == 2)
        pole_binary = np.concatenate([ones,twos])
        return pole_binary

    def binaryToTrinaryBoard(self,pole_binary,sites = 30):
        return pole_binary[0:sites]*1 + pole_binary[sites:2*sites]*2

    def binaryBoardToInt(self,pole_binary):
        #print(pole_binary)
        #s = '0b' + ''.join(['1' if v else '0' for v in pole_binary])
        s = ''.join(['1' if v else '0' for v in pole_binary])
        c = int(s,2)
        return c

    def intToBinaryBoard(self,pole_int, sites = 30):
        binary_literal = bin(pole_int)
        l = list(binary_literal[2:])
        #filling in zeros to full board
        l = [0]*(2*sites - len(l)) + l
        binary_board = (np.array(l).astype(np.int64) == 1)
        return binary_board

    def intToTrinaryBoard(self,pole_int, sites = 30):
        pole_binary = self.intToBinaryBoard(pole_int, sites = sites)
        return self.binaryToTrinaryBoard(pole_binary, sites = sites)

    def trinaryBoardToInt(self,pole_trinary):
        pole_binary = self.trinaryToBinaryBoard(pole_trinary)
        return self.binaryBoardToInt(pole_binary)

    ###########################################################################

    def bigAnd(self,l): #and between all elements of a list of bools
        return (np.sum(l) == len(l))

    def bigAllFalse(self,l): #all elements of the array must be False
        return (np.sum(l) == 0)

    def availablePositions(self,pole_trinary, base = range(14,30)):

        #0
        #
        #1  2
        #3  4
        #
        # 5  6  7
        # 8  9  10
        # 11 12 13
        #
        # 14 15 16 17
        # 18 19 20 21
        # 22 23 24 25
        # 26 27 28 29

        #need to specify dependencies:
        dependencies = {
        11: [22,23,26,27],
        12: [23,24,27,28],
        13: [24,25,28,29],
        8: [18,19,22,23],
        9: [19,20,23,24],
        10: [20,21,24,25],
        5: [14,15,18,19],
        6: [15,16,19,20],
        7: [16,17,20,21],

        1: [5,6,8,9],
        2: [6,7,9,10],
        3: [8,9,11,12],
        4: [9,10,12,13],

        0: [1,2,3,4]
        }

        pole = np.array(pole_trinary)
        plno = (pole != 0)

        available = np.zeros_like(plno).astype(bool)

        for position in dependencies:
            if not plno[position]: #is empty so that it can be available for a move
                parents = dependencies[position]
                stability = self.bigAnd(plno[parents])
                available[position] = stability

        #also look at the base layer
        for position in base:
            if not plno[position]:
                available[position] = True

        return available

    def canSafelyRemove(self,pole_trinary, sites = 30): #list of bools if can safely remove from stability and also occupied

        #0
        #
        #1  2
        #3  4
        #
        # 5  6  7
        # 8  9  10
        # 11 12 13
        #
        # 14 15 16 17
        # 18 19 20 21
        # 22 23 24 25
        # 26 27 28 29

        dependencies = {
        0: [],

        1: [0],
        2: [0],
        3: [0],
        4: [0],

        5: [1],
        6: [1,2],
        7: [2],
        8: [1,3],
        9: [1,2,3,4],
        10: [2,4],
        11: [3],
        12: [3,4],
        13: [4],

        14: [5],
        15: [5,6],
        16: [6,7],
        17: [7],
        18: [5,8],
        19: [5,6,8,9],
        20: [6,7,9,10],
        21: [7,10],
        22: [8,11],
        23: [8,9,11,12],
        24: [9,10,12,13],
        25: [10,13],
        26: [11],
        27: [11,12],
        28: [12,13],
        29: [13]
        }

        pole = np.array(pole_trinary)
        plno = (pole != 0)

        canremove = np.zeros_like(plno).astype(bool)

        for position in range(sites):
            if plno[position]:
                children = dependencies[position]
                can = self.bigAllFalse(plno[children])
                canremove[position] = can

        return canremove

    def specialShapeMade(self,pole_now,pole_past,player): #determines if player created special shape


        specials = [

        #0
        #
        #1  2
        #3  4
        #
        # 5  6  7
        # 8  9  10
        # 11 12 13
        #
        # 14 15 16 17
        # 18 19 20 21
        # 22 23 24 25
        # 26 27 28 29

        #ctverce 1
        [1,2,3,4],

        #ctverce 2
        [5,6,8,9],
        [6,7,9,10],
        [8,9,11,12],
        [9,10,12,13],

        #ctverce 3
        [14,15,18,19],
        [15,16,19,20],
        [16,17,20,21],
        [18,19,22,23],
        [19,20,23,24],
        [20,21,24,25],
        [22,23,26,27],
        [23,24,27,28],
        [24,25,28,29],

        #0
        #
        #1  2
        #3  4
        #
        # 5  6  7
        # 8  9  10
        # 11 12 13
        #
        # 14 15 16 17
        # 18 19 20 21
        # 22 23 24 25
        # 26 27 28 29

        #radky 2
        [5,6,7],
        [8,9,10],
        [11,12,13],
        [5,8,11],
        [6,9,12],
        [7,10,13],
        [5,9,13],
        [7,9,11],

        #radky 3
        [14,15,16,17],
        [18,19,20,21],
        [22,23,24,25],
        [26,27,28,29],
        [14,18,22,26],
        [15,19,23,27],
        [16,20,24,28],
        [17,21,25,29],
        [14,19,24,29],
        [17,20,23,26]

        ]

        now = np.array(pole_now)
        past = np.array(pole_past)

        change = np.logical_not(np.equal(now,past)) #where changes happened, otherwise would have to check everything all the time
        changed_indices = [i for i,x in enumerate(change) if x]
        changed_indices_set = set(changed_indices)

        #special configurations that are potentially changed
        specials_changed = []

        for i,special in enumerate(specials):

            special_changed = (list(changed_indices_set.intersection(special)) != [])
            specials_changed.append(i)


        special_activated = False
        special_activated_indices = None

        #list of special configuration indices in specials that are potentially changed
        for i in specials_changed:
            special = specials[i]

            shape_bool_now = self.bigAnd(now[special] == player)
            shape_bool_past = self.bigAnd(past[special] == player)

            if ((shape_bool_now) and not(shape_bool_past)): #if wasn't and now is special
                special_activated = True
                special_activated_indices = special
                break

        return special_activated, special_activated_indices


    def turnPlayer(self,player):
        if player == 1:
            return 2
        elif player == 2:
            return 1
        else:
            return None

    def getLevel(self,p):
        if p in [0]:
            return 0
        elif p in list(range(1,5)):
            return 1
        elif p in list(range(5,14)):
            return 2
        elif p in list(range(14,30)):
            return 3
        else:
            None

    def getNextSteps(self,pole_trinary,player): #generate a list of actions that can be taken by player

        player1_count = np.sum(pole_trinary == 1)
        player2_count = np.sum(pole_trinary == 2)

        nextSteps = [] #(player)

        nextStepsCurated = [] #just if the if is False

        #if current playet hasn't run out of balls
        if (((player == 1) and (player1_count<15)) or ((player == 2) and (player2_count<15))):

            #ordinary moves first
            available_positions = self.availablePositions(pole_trinary)
            available_positions_list = [i for i,x in enumerate(available_positions) if x]

            for p in available_positions_list:
                pole_modified = np.array(pole_trinary) #reset to the actual board now
                pole_modified[p] = player

                nextSteps.append(
                    (
                    self.turnPlayer(player), #next player
                    ("move",player,p,None), #action specification
                    self.trinaryBoardToInt(pole_modified) #int of the next board
                    )
                )


            #jumps
            canremove_stability = self.canSafelyRemove(pole_trinary)
            canremove_stability_list = [i for i,x in enumerate(canremove_stability) if x]
            canremove = [p for p in canremove_stability_list if pole_trinary[p] == player]
            for r in canremove:
                r_level = self.getLevel(r)
                pole_modified = np.array(pole_trinary)
                pole_modified[r] = 0 #removing stone
                available_positions_modified = self.availablePositions(pole_modified)
                available_positions_modified_list = [i for i,x in enumerate(available_positions_modified) if x]
                for i in available_positions_modified_list:
                    i_level = self.getLevel(i)
                    if ((r_level > i_level) and (i != r)):
                        pole_modified2 = np.array(pole_modified)
                        pole_modified2[i] = player #adding stope

                        nextSteps.append(
                            (
                            self.turnPlayer(player), #next player
                            ("jump",player,r,i), #action specification
                            self.trinaryBoardToInt(pole_modified2) #int of the next board
                            )
                        )

            #--------------------------------------------------------
            #new moves are now generated by simple moves and jumps
            #stored in nextSteps
            #will generate nextStepsCurated that will have special shapes collected

            nextStepsCurated = []

            #detecting special shapes
            for i,nextStep in enumerate(nextSteps):
                (newplayer,descriptions,pole_new_int) = nextStep
                pole_new = self.intToTrinaryBoard(pole_new_int)

                is_special, which = self.specialShapeMade(pole_new,pole_trinary,player)

                if not is_special: #no special shape, just continuing
                    nextStepsCurated.append(nextStep)

                elif is_special: #special shape was made by a move, now can remove 0,1, or 2 player's balls

                    # print(descriptions,"*****************")
                    # print(which)
                    # print("Puvodni:")
                    # showTrinaryBoard(pole_trinary)
                    # print("Nove:")
                    # showTrinaryBoard(pole_new)

                    #option 0, removing 0 stones = doing nothing
                    descriptions_new = (descriptions[0]+"-r0",descriptions[1],descriptions[2],descriptions[3])
                    nextStepsCurated.append(
                        (
                        newplayer,
                        descriptions_new,
                        pole_new_int
                        )
                    )

                    #option 1 and 2, removing 1 or 2 stones
                    canremove_stability = self.canSafelyRemove(pole_new)
                    canremove_stability_list = [i for i,x in enumerate(canremove_stability) if x]
                    canremove = [p for p in canremove_stability_list if pole_new[p] == player]
                    for r in canremove:
                        pole_modified = np.array(pole_new)
                        pole_modified[r] = 0 #removing stone

                        #removing 1 stone
                        descriptions_new = (descriptions[0]+"-r1p"+str(r),descriptions[1],descriptions[2],descriptions[3])
                        nextStepsCurated.append(
                            (
                            newplayer,
                            descriptions_new,
                            self.trinaryBoardToInt(pole_modified)
                            )
                        )

                        #removing another stone
                        canremove_stability2 = self.canSafelyRemove(pole_modified)
                        canremove_stability2_list = [i for i,x in enumerate(canremove_stability2) if x]
                        canremove2 = [p for p in canremove_stability2_list if pole_modified[p] == player]

                        for r2 in canremove2:
                            pole_modified2 = np.array(pole_modified)
                            pole_modified2[r2] = 0 #removing stone

                            #removing another stone (2nd) stone
                            descriptions_new2 = (descriptions[0]+"-r2p"+str(r)+"p"+str(r2),descriptions[1],descriptions[2],descriptions[3])
                            nextStepsCurated.append(
                                (
                                newplayer,
                                descriptions_new2,
                                self.trinaryBoardToInt(pole_modified2)
                                )
                            )




        return nextStepsCurated


    def Wins(self,pole_trinary):

        if np.sum(pole_trinary != 0) == 30: #board full
            return pole_trinary[0]
        elif np.sum(pole_trinary == 1) == 15: #player 1 ran out of stones
            return 2
        elif np.sum(pole_trinary == 2) == 15: #player 2 ran out of stones
            return 1
        else:
            return None

class randomAgent(object):

    def __init__(self):
        self.name = "Random Agent"
        self.description = "Chooses actions at random."
        return None

    def takeAction(self,player,game,pole_int):

        pole_trinary = game.intToTrinaryBoard(pole_int)
        nextSteps = game.getNextSteps(pole_trinary,player)

        if len(nextSteps) == 0: #no steps available
            return None
        else:
            random_index = np.random.choice(range(len(nextSteps)))

            (newplayer,name,pole_new_int) = nextSteps[random_index]

            return pole_new_int

def simpleBoardEvaluator(player,game,pole_int):
    #just looks at the difference in the number of stones and uses that as score

    pole3 = game.intToTrinaryBoard(pole_int)

    number_mine = np.sum(pole3 == player)
    number_opponent = np.sum(pole3 == game.turnPlayer(player))

    return number_opponent - number_mine

# def slightlyBetterBoardEvaluator(player,game,pole_int):
#     #gives higher weight to smaller levels of the pyramid
#     a = 5.0
#     b = 3.0
#     c = 2.0
#     d = 1.0
#
#     weights = np.array([
#     a,
#     b,b,
#     b,b,
#     c,c,c,
#     c,c,c,
#     c,c,c,
#     d,d,d,d,
#     d,d,d,d,
#     d,d,d,d,
#     d,d,d,d
#     ])
#
#     pole3 = game.intToTrinaryBoard(pole_int)
#
#     score_mine = np.sum((pole3 == player).astype(float)*weights)
#     score_opponent = np.sum((pole3 == game.turnPlayer(player)).astype(float)*weights)
#
#     return score_opponent - score_mine

def slightlyBetterBoardEvaluator(player,game,pole_int):
    #gives higher weight to smaller levels of the pyramid
    #bonus for stones higher up

    pole3 = game.intToTrinaryBoard(pole_int)

    stones_mine = (pole3 == player)
    stones_opponent = (pole3 == game.turnPlayer(player))

    #just difference in number of stones on the board
    score_number = np.sum(stones_opponent) - np.sum(stones_mine)


    level_ranges = [[0],range(1,5),range(5,14),range(14,30)]

    levels_mine = np.array([np.sum(pole3[level_ranges[l]] == player) for l in range(4)])
    levels_opponent = np.array([np.sum(pole3[level_ranges[l]] == game.turnPlayer(player)) for l in range(4)])

    bonus_mine = np.sum(np.array([0.5,0.4,0.3,0.0])*levels_mine)
    bonus_opponent = np.sum(np.array([0.5,0.4,0.3,0.0])*levels_opponent)
    score_bonuses = bonus_mine - bonus_opponent

    return score_number + score_bonuses

class simpleAgent(object):

    def __init__(self):
        self.name = "Simple Agent"
        self.description = "Number of stones, looks one step ahead."
        return None

    # def evaluateBoard(self,player,game,pole_int):
    #
    #     pole3 = game.intToTrinaryBoard(pole_int)
    #
    #     number_mine = np.sum(pole3 == player)
    #     number_opponent = np.sum(pole3 == game.turnPlayer(player))
    #
    #     return number_opponent - number_mine

    def evaluateBoard(self,player,game,pole_int):
        #return simpleBoardEvaluator(player,game,pole_int)
        return slightlyBetterBoardEvaluator(player,game,pole_int)

    def takeAction(self,player,game,pole_int):

        pole_trinary = game.intToTrinaryBoard(pole_int)
        nextSteps = game.getNextSteps(pole_trinary,player)

        values = []

        for nextStep in nextSteps:
            (_,_,pole_new_int) = nextStep
            value = self.evaluateBoard(player,game,pole_new_int)
            values.append(value)

        max_index = np.argmax(values)

        (newplayer,name,pole_new_int) = nextSteps[max_index]

        return pole_new_int

class miniMaxAgent(object):

    def __init__(self,depth):
        self.depth = depth
        self.name = "MiniMax Agent"
        self.description = "Looks depth "+str(depth)+" ahead, uses number of stones."
        return None

    # def evaluateBoard(self,player,game,pole_int):
    #
    #     pole3 = game.intToTrinaryBoard(pole_int)
    #
    #     number_mine = np.sum(pole3 == player)
    #     number_opponent = np.sum(pole3 == game.turnPlayer(player))
    #
    #     return number_opponent - number_mine

    def evaluateBoard(self,player,game,pole_int):
        #return simpleBoardEvaluator(player,game,pole_int)
        return slightlyBetterBoardEvaluator(player,game,pole_int)

    def miniMax(self,player_root,player_now,game,pole_int_now,d):

        pole_trinary = game.intToTrinaryBoard(pole_int_now)

        large_number_win = 100.0
        negative_large_number_loss = -100.0

        #victory by putting stone on top or opponent running out of stones (specified in game.Win)
        if (game.Wins(pole_trinary) in [1,2]):
            if game.Wins(pole_trinary) == player_root:
                return large_number_win
            elif game.Wins(pole_trinary) == game.turnPlayer(player_root):
                return negative_large_number_loss
        #leaf reached
        elif d == 0:
            return self.evaluateBoard(player_now,game,pole_int_now)
        #not leaf
        elif d>0:
            pole_trinary = game.intToTrinaryBoard(pole_int_now)
            nextSteps = game.getNextSteps(pole_trinary,player_now)

            if player_root == player_now:
                #print([self.miniMax(player_root,game.turnPlayer(player_now),game,nextStep[2],d-1) for nextStep in nextSteps])
                return np.amax([self.miniMax(player_root,game.turnPlayer(player_now),game,nextStep[2],d-1) for nextStep in nextSteps])
            elif player_root == game.turnPlayer(player_now):
                #print([self.miniMax(player_root,game.turnPlayer(player_now),game,nextStep[2],d-1) for nextStep in nextSteps])
                return np.amin([self.miniMax(player_root,game.turnPlayer(player_now),game,nextStep[2],d-1) for nextStep in nextSteps])


    def takeAction(self,player,game,pole_int):

        pole_trinary = game.intToTrinaryBoard(pole_int)
        nextSteps = game.getNextSteps(pole_trinary,player)

        values = []

        for nextStep in nextSteps:
            (_,_,pole_new_int) = nextStep
            #value = self.evaluateBoard(player,game,pole_new_int)
            value = self.miniMax(player,player,game,pole_new_int,self.depth)
            values.append(value)

        max_index = np.argmax(values)

        (newplayer,name,pole_new_int) = nextSteps[max_index]

        return pole_new_int



def testAgents(game,N,agent1,agent2,maxt = 1000,verbose = True):

    print("Overview:")
    print("Agent 1 =",agent1.name)
    print(agent1.description)
    print("Agent 2 =",agent2.name)
    print(agent2.description)
    print("----------")
    print("max plies =",maxt)
    print("----------")


    number_win1 = 0
    number_win2 = 0

    for n in range(N):

        empty_board = [
        0,
        0,0,
        0,0,
        0,0,0,
        0,0,0,
        0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0
        ]

        #initial configuration
        pole = np.array(empty_board)
        pole_int = game.trinaryBoardToInt(pole)
        player = 1

        t = 0
        while ((game.Wins(game.intToTrinaryBoard(pole_int)) is None) and (t<maxt)):
            #print(t,player,pole_int)
            if verbose:
                #game stats
                pole_tri = game.intToTrinaryBoard(pole_int)
                print("ply "+str(t)+" #1="+str(np.sum(pole_tri == 1))+"#2="+str(np.sum(pole_tri == 2)))
                game.showTrinaryBoard(pole_tri)

            if player == 1:
                pole_new_int = agent1.takeAction(player,game,pole_int)
                if pole_new_int is not None:
                    t += 1
                    pole_int = pole_new_int
                    player = game.turnPlayer(player)
                else:
                    print("Player ",player,"has no moves available.")
            elif player == 2:
                pole_new_int = agent2.takeAction(player,game,pole_int)
                if pole_new_int is not None:
                    t += 1
                    pole_int = pole_new_int
                    player = game.turnPlayer(player)
                else:
                    print("Player ",player,"has no moves available.")
            else:
                print("Invalidat player =",player)

        if t<maxt:
            winner = game.Wins(game.intToTrinaryBoard(pole_int))

            if winner == 1:
                number_win1 += 1
            elif winner == 2:
                number_win2 += 1

            number_draws = n + 1 - number_win1 - number_win2
            print("trial",n,"plies =",t,"Wins =",winner,"overall stats",number_win1,number_draws,number_win2)

        else:
            print("trial",n,"Max plies reached.")

###########################################
#testing

game = classGame()

agent1 = randomAgent()
agent2 = simpleAgent()
#agent2 = miniMaxAgent(depth = 2)

testAgents(game,1000,agent1,agent2,maxt = 500,verbose = False)
