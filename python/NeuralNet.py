import discord
import numpy as np
import math
import datetime
import asyncio
import random
from itertools import cycle
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from discord.utils import get
import copy

client = commands.Bot(command_prefix='.')
client.remove_command('help')

timers = {}
mutedict = {}
ping = {}
unmuteds = []

randommsgleft = random.randint(1, 6)
randmsg = ['ok boomer', 'that\'s insane!', 'WHAAATT!??!', 'wut', 'and?', 'so?', 'i know u are but what am i?',
           'i\'ve got nothing else', 'bless you', '^w^', 'agreed', 'names noted']
random.shuffle(randmsg)
randmsglist = cycle(randmsg)


class Neuron:

    def __init__(self, type, num, extra=None):
        self.type = type
        self.extra = extra
        self.weights = []
        for i in range(num):
            self.weights.append(random.random())
        self.bias = random.random()
        self.weights = np.array(self.weights)

    def activation(self, inputs):
        if self.type == 'softmax':
            return self.softmax(inputs)

        sum = 0
        for i in range(len(inputs)):
            sum += inputs[i] * self.weights[i]
        sum += self.bias

        if self.type == 'relu':
            return self.relu(sum)
        elif self.type == 'sigmoid':
            return self.sigmoid(sum)

    def relu(self, num):
        if num < 0:
            return 0
        return num

    def sigmoid(self, num):
        return 1 / (1 + math.pow(math.e, -1 * num))

    def softmax(self, inputs):
        sum = 0
        for i in range(len(inputs)):
            sum += math.pow(math.e, inputs[i] * self.weights[i])
        return math.pow(math.e, inputs[self.extra]) / sum


class NeuralNet:

    def __init__(self, neurons, turn):
        self.layers = []
        self.turn = turn
        for j in range(neurons):
            temp = []
            for i in range(9):
                temp.append(Neuron("relu", 9))
            temp = np.array(temp)
            self.layers.append(temp)
        temp = []
        for i in range(9):
            # print("hecc")
            # print(len(self.layers[len(self.layers) - 1]))
            temp.append(Neuron("softmax", len(self.layers[len(self.layers) - 1]), i))
        self.layers.append(temp)
        self.layers = np.array(self.layers)

    def run(self, inputs):
        flattened = []
        for r in inputs:
            for c in r:
                if self.turn == c:
                    flattened.append(1)
                elif self.turn != ' ':
                    flattened.append(0)
                else:
                    flattened.append(-1)

        newInputs = flattened
        for layer in self.layers:
            temp = []
            # print(f"layers: {len(layer)} inputs: {len(newInputs)}")
            for neuron in layer:
                temp.append(neuron.activation(newInputs))
            newInputs = temp

        small = 0
        spot = 0
        for i in range(len(newInputs)):
            if newInputs[i] > small:
                small = newInputs[i]
                spot = i

        return [int(spot / 3), spot % 3]

    def train(self, inputs, ifprint=False):
        outputs = []
        flattened = []
        for r in inputs:
            for c in r:
                if self.turn == c:
                    flattened.append(1)
                elif self.turn != ' ':
                    flattened.append(0)
                else:
                    flattened.append(-1)

        outputs.append(flattened)
        oldWeights = []
        oldBias = []

        newInputs = flattened
        for layer in self.layers:
            temp = []
            tempo = []
            tempb = []
            for neuron in layer:
                temp.append(neuron.activation(newInputs))
                tempo.append(neuron.weights)
                tempb.append(neuron.bias)
            oldWeights.append(tempo)
            oldBias.append(tempb)
            newInputs = temp
            outputs.append(newInputs)

        small = 0
        spot = 0
        for i in range(len(newInputs)):
            if newInputs[i] > small:
                small = newInputs[i]
                spot = i

        hecc = bestMove(inputs, self.turn)
        bm = hecc[0] * 3 + hecc[1] % 3

        if bm == spot:
            return [int(spot / 3), spot % 3]

        error = []
        for i in range(9):
            if i == bm:
                error.append(1 - newInputs[i])
            else:
                error.append(0 - newInputs[i])

        error = np.array(error)
        outputs = np.array(outputs)
        oldWeights = np.array(oldWeights)
        # print(oldWeights)

        if ifprint or ifprint == "True":
            print(f"Error: {np.mean(error)} Guess: {spot} P: {newInputs}")

        num = len(self.layers)

        currError = error
        oldDelta = self.getDelta(error, outputs[num])
        while num != 0:
            if num != len(self.layers):
                currError = self.getError(oldDelta, oldWeights[num - 1])
            oldDelta = self.getDelta(currError, outputs[num])
            oldWeights[num - 1] -= np.dot(outputs[num - 1].T, oldDelta)
            num -= 1

        # print(oldWeights)

        for layer in range(len(oldWeights)):
            for neuronWeights in range(len(oldWeights[layer])):
                # print(self.layers[layer][neuronWeights].weights)
                # print(oldWeights[layer][neuronWeights])
                self.layers[layer][neuronWeights].weights = oldWeights[layer][neuronWeights]

        return [int(spot / 3), spot % 3]

    def export(self):
        weights = []
        bias = []

        for layer in self.layers:
            tempo = []
            tempb = []
            for neuron in layer:
                tempo.append(neuron.weights)
                tempb.append(neuron.bias)
            weights.append(tempo)
            bias.append(tempb)

        weights = np.array(weights)
        bias = np.array(bias)

        return "Weights: \n" + str(weights) + "\n\n Bias: \n" + str(bias)

    def importWeights(self, weights):
        print(weights)

        for layer in range(len(self.layers)):
            for neuron in range(len(self.layers[layer])):
                # print(len(weights))
                # print(len(self.layers))
                self.layers[layer][neuron].weights = weights[layer][neuron]

    def importBias(self, bias):
        for layer in range(len(self.layers)):
            for neuron in range(len(self.layers[layer])):
                # print(len(weights))
                # print(len(self.layers))
                self.layers[layer][neuron].bias = bias[layer][neuron]

    def getDeriv(self, inp):
        inp = np.array(inp)
        return inp * (1 - inp)

    def getDelta(self, error, output):
        return error * self.getDeriv(output)

    def getError(self, oldDelta, weights):
        return np.dot(oldDelta, weights.T)


def indexOf(s, o):
    try:
        return s.index(o)
    except ValueError:
        return -1


async def randmsg(self):
    global randommsgleft
    global randmsglist
    global randmsg
    print(randommsgleft, "messages left")
    if randommsgleft == 0:
        print('sent')
        await self.channel.send(next(randmsglist))
        randommsgleft = random.randint(5, 30)
    else:
        randommsgleft -= 1


@tasks.loop(seconds=60)
async def timeloop():
    print('loop')


@client.event
async def on_ready():
    print('Let\'s gET ReAdY tO RuMBlE')
    await client.change_presence(activity=discord.Game('Hello!'))
    timeloop.start()


@client.event
async def on_member_join(member):
    print(f'{member} has joined the a server')


@client.event
async def on_member_remove(member):
    print(f' Hello, {member} I\'m a bot thing!')


@client.event
async def on_message(self):
    if self.author.id != 671561651027312643 and indexOf(self.content, '.') != 0:
        if indexOf(self.content.lower(), 'gn') > -1 or indexOf(self.content.lower(), 'good night') > -1:
            await self.channel.send("Good Night!")
        else:
            await randmsg(self)
    await client.process_commands(self)


@client.command()
async def ding(ctx):
    await ctx.send('Dong!')


NN = None
board = None


@client.command()
async def tictactoe(ctx, n=1):
    global board
    global NN

    NN = NeuralNet(n, 'x')

    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    print(f"Guess: {NN.train(board, True)} Real: {bestMove(board, 'x')}")

    await ctx.send('Initialized!')


@client.command()
async def train(ctx, gen, games=20, err=False):
    global NN
    global board

    NN.turn = 'x'

    for i in range(int(gen)):
        win = 0
        for x in range(int(games)):
            board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            ran = random.randint(0, 1)
            turns = 0
            fail = 0
            NN.turn = 'x'
            if ran == 0:
                turns = 1
            while checkW(board) == ' ':
                if turns == 1:
                    move = NN.train(board, err)
                    if board[move[0]][move[1]] != ' ':
                        fail = 1
                        pos = []
                        for r in range(0, 3):
                            for c in range(0, 3):
                                if board[r][c] == ' ':
                                    pos.append([r, c])
                        pic = random.randint(0, len(pos) - 1)
                        board[pos[pic][0]][pos[pic][1]] = 'x'
                    else:
                        board[move[0]][move[1]] = NN.turn
                    turns = 0
                else:
                    if random.randint(0, 10) == 0:
                        pos = []
                        for r in range(0, 3):
                            for c in range(0, 3):
                                if board[r][c] == ' ':
                                    pos.append([r, c])
                        pic = random.randint(0, len(pos) - 1)
                        board[pos[pic][0]][pos[pic][1]] = 'o'
                    else:
                        pic = bestMove(board, 'o')
                        board[pic[0]][pic[1]] = 'o'
                    turns = 1
            if checkW(board) == NN.turn or checkW(board) == 'tie' and fail == 1:
                win += 1
        print(f"Generation {i}: Success Rate: {float(win) / games}")

    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    await ctx.send("done!")


@client.command()
async def export(ctx, best=None):
    if NN is not None:
        f = open("temp.txt", "w")
        f.write(NN.export())
        f.close()
        if best == "best":
            f = open("best.txt", "w")
            f.write(NN.export())
            f.close()
            await ctx.send("exported Best :D")
        else:
            await ctx.send("exported")


@client.command()
async def best(ctx):
    # weights = np.array([[[1.61068736e-01, 1.49563871e-01, -1.28954791e-01, -2.66550043e-01, 9.15673722e-02, -1.87259344e-01, 5.86959963e-02, 3.15766324e-01, 1.26720495e-01], [-2.06127696e-01, -4.10522709e-01, -2.05890690e-01, -2.53696215e-01, 2.75279824e-01, -2.58662318e-01, -3.23652421e-01, 9.05166021e-02, 1.86133389e-01], [-1.39691340e-02, -6.00892550e-01, -4.85666460e-01, -2.46411649e-01, -4.74939535e-01, -5.71241248e-01, -6.06203080e-01, -3.10420989e-01, -2.64657064e-01], [3.50249993e-01, -5.15541330e-01, -2.16577077e-01, -2.31443501e-01, 1.33319262e-01, -9.25489561e-02, -4.25534481e-02, -4.60149666e-01, -2.83374716e-01],[2.07654125e-04, -1.20911822e-01, -4.89803435e-01, -3.75316340e-01, -5.32823305e-01, -1.03784026e-01, 3.68219994e-01, -5.15276969e-01, 3.20531555e-01],[-4.79791708e-01, 4.85080211e-02, -1.56938364e-01, -5.26084623e-01, 3.16934890e-01, -5.85570926e-01, 2.01469463e-01, 1.37471287e-01, 2.45865346e-01],[-5.53437954e-01, 1.47850374e-01, -4.61254355e-01, -2.43005837e-02, 1.88948012e-01, -9.29911891e-02, 5.87680230e-02, 5.94368213e-02 - 3.12850347e-01],[2.11118616e-01, 2.54607171e-04, 6.40421184e-02, -4.75468925e-01, -4.55355022e-01, 3.30441148e-01, 1.41825301e-01, -1.19061182e-01, 1.86665269e-01], [-2.83073809e-01, -3.52804307e-01, 9.65419807e-03, -4.50655598e-01, -3.50660873e-01, -2.89641402e-01, -1.18538751e-01, -4.28042587e-02, 2.25781112e-01]], [[1.06807950e+00, 1.76143953e+00, 1.01256695e+00, 1.22586447e+00, 1.11412501e+00, 1.05375645e+00, 1.76823567e+00, 1.79845080e+00, 1.35153566e+00],[1.42365510e+00, 8.58320941e-01, 1.23099055e+00, 9.57959236e-01, 8.74689471e-01, 8.98886027e-01, 1.23131211e+00, 1.38942325e+00, 1.57012777e+00],[1.48289694e+00, 1.06906747e+00, 1.16193058e+00, 9.27473484e-01, 1.19376374e+00, 1.02247633e+00, 1.38632704e+00, 1.02912734e+00, 1.50272058e+00],[9.98876642e-01, 1.33848626e+00, 1.11471567e+00, 1.42415314e+00, 1.67108966e+00, 1.14786588e+00, 1.01802851e+00, 1.61168367e+00, 1.14629372e+00],[1.67020409e+00, 1.32645699e+00, 1.69786250e+00, 1.52609185e+00, 1.05961156e+00, 1.09418867e+00, 1.16384083e+00, 1.03172135e+00, 1.25090569e+00],[1.39462545e+00, 1.77812479e+00, 1.06767252e+00, 1.68901843e+00, 1.37095698e+00, 1.53955809e+00, 1.19734074e+00, 1.63692928e+00, 1.52424002e+00],[1.39659368e+00, 8.92957888e-01, 1.67054062e+00, 1.49921815e+00, 1.65683361e+00, 1.77180061e+00, 1.37677904e+00, 1.46058853e+00, 1.31390776e+00],[1.25597699e+00, 1.69664355e+00, 1.70279048e+00, 1.21968841e+00, 8.32914534e-01, 1.31143168e+00, 1.01448053e+00, 9.68531140e-01, 1.34384513e+00],[1.64406948e+00, 1.24158625e+00, 1.28438524e+00, 1.27678853e+00, 9.81434709e-01, 1.63800198e+00, 1.42895060e+00, 8.84806192e-01, 1.70811523e+00]]])
    # bias = np.array([[0.22747307, 0.83939365, 0.97892022, 0.99735734, 0.82799479, 0.79629123,0.24296053, 0.04336028, 0.97637616], [0.54387014, 0.08866272, 0.12594727, 0.16973761, 0.43010673, 0.92042279,0.99935033, 0.3619859, 0.14450607]])

    stri1 = ""
    stri2 = ""
    f = open("temp.txt", "r")
    w = 0
    for i in f:
        # print(i)
        if i.__contains__("Weights"):
            print("hihihihihihi")
            w = 1
        elif i.__contains__("Bias"):
            w = 2
        elif w == 1:
            stri1 += i
        elif w == 2:
            stri2 += i

    print(stri1)
    # print(stri2)

    flist1 = stri1.split(" [[")
    finlist = []
    for i in range(len(flist1)):
        temp2 = flist1[i].split("]\n  [")

        for x in range(len(temp2)):
            st = temp2[x]
            st = st.replace("[", "")
            st = st.replace("(", "")
            st = st.replace("array", "")
            st = st.replace("]", "")
            st = st.replace(")", "")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")

            temp2[x] = st.split(" ")
            for i in temp2[x]:
                if i == '':
                    temp2[x].remove(i)

        # print(temp2)
        finlist.append(temp2)

        # print(temp2)

    print(finlist)

    for l in range(len(finlist)):
        for r in range(len(finlist[l])):
            for c in range(len(finlist[l][r])):
                finlist[l][r][c] = float(finlist[l][r][c])

    finlist = np.array(finlist)
    print(finlist)

    # print(str)
    if NN is not None:
        NN.importWeights(finlist)

    flist1 = stri2.split(" [")
    finlist = []
    for i in range(len(flist1)):
        st = flist1[i]
        st = st.replace("[", "")
        st = st.replace("(", "")
        st = st.replace("array", "")
        st = st.replace("]", "")
        st = st.replace(")", "")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("  ", " ")
        st = st.replace("\n", "")
        finlist.append(st.split(" "))
        for j in finlist[i]:
            if j == '':
                finlist[i].remove(j)

    for l in range(len(finlist)):
        for r in range(len(finlist[l])):
            finlist[l][r] = float(finlist[l][r])

    finlist = np.array(finlist)
    print(finlist)
    if NN is not None:
        NN.importBias(finlist)
        await ctx.send("Imported")


@client.command()
async def imports(ctx, type, *weights):
    if type == "bias":
        stri = ""
        for i in weights:
            stri += i + " "
        # print(str)
        flist1 = stri.split(" [")
        finlist = []
        for i in range(len(flist1)):
            st = flist1[i]
            st = st.replace("[", "")
            st = st.replace("(", "")
            st = st.replace("array", "")
            st = st.replace("]", "")
            st = st.replace(")", "")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            st = st.replace("  ", " ")
            finlist.append(st.split(" "))
            for j in finlist[i]:
                if j == '':
                    finlist[i].remove(j)

        finlist = np.array(finlist)
        print(finlist)
        if NN is not None:
            NN.importBias(finlist)
            await ctx.send("Imported Bias")
    if type == "weights":
        stri = ""
        for i in weights:
            stri += i + " "
        # print(str)
        flist1 = stri.split(" [[")
        finlist = []
        for i in range(len(flist1)):
            temp2 = flist1[i].split("] [")

            for x in range(len(temp2)):
                st = temp2[x]
                st = st.replace("[", "")
                st = st.replace("(", "")
                st = st.replace("array", "")
                st = st.replace("]", "")
                st = st.replace(")", "")
                st = st.replace("  ", " ")
                st = st.replace("  ", " ")
                st = st.replace("  ", " ")
                st = st.replace("  ", " ")
                temp2[x] = st.split(" ")
                for i in temp2[x]:
                    if i == '':
                        temp2[x].remove(i)

            # print(temp2)
            finlist.append(temp2)

            # print(temp2)

        print(finlist)

        for l in range(len(finlist)):
            for r in range(len(finlist[l])):
                for c in range(len(finlist[l][r])):
                    finlist[l][r][c] = float(finlist[l][r][c])

        finlist = np.array(finlist)

        # print(str)
        if NN is not None:
            NN.importWeights(finlist)
            await ctx.send("Imported Weights")


playturn = 'x'


@client.command()
async def reset(ctx):
    global board
    global playturn
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    playturn = 'x'
    await ctx.send("Reset!")


@client.command()
async def play(ctx, spot):
    global playturn
    global board
    global NN
    NN.turn = 'o'
    spot = int(spot)
    spot -= 1

    if spot < 9 and board[int(spot / 3)][spot % 3] == ' ':
        board[int(spot / 3)][spot % 3] = playturn

        if playturn == 'x':
            playturn = 'o'
        else:
            playturn = 'x'

        stri = ""
        if checkW(board) == ' ':
            # x = bestMove(board, turn)
            x = NN.run(board)
            if board[x[0]][x[1]] != ' ':
                pos = []
                for r in range(0, 3):
                    for c in range(0, 3):
                        if board[r][c] == ' ':
                            pos.append([r, c])
                pic = random.randint(0, len(pos) - 1)
                board[pos[pic][0]][pos[pic][1]] = NN.turn
            else:
                board[x[0]][x[1]] = NN.turn
            if checkW(board) != ' ':
                stri = "someone won \n"
            if playturn == 'x':
                playturn = 'o'
            else:
                playturn = 'x'
            for i in range(len(board)):
                for j in range(len(board)):
                    stri += board[i][j] + ", "
                stri += "\n"
            stri += "\n"
        else:
            stri = "someone won \n"
            for i in range(len(board)):
                for j in range(len(board)):
                    stri += board[i][j] + ", "
                stri += "\n"
            stri += "\n"

        await ctx.send(stri + " ")
    else:
        await ctx.send("invalid spot")


def checkW(input):
    for r in input:
        if r[0] == r[1] == r[2] and r[0] != ' ':
            return r[0]

    for i in range(0, len(input)):
        if input[0][i] == input[1][i] == input[2][i] and input[0][i] != ' ':
            return input[0][i]

    if input[0][0] == input[1][1] == input[2][2] and input[1][1] != ' ':
        return input[1][1]

    if input[2][0] == input[1][1] == input[0][2] and input[1][1] != ' ':
        return input[1][1]

    for r in input:
        for c in r:
            if c == ' ':
                return ' '

    return 'tie'


def bestMove(input, player):
    bestScore = -math.inf
    move = []
    for i in range(3):
        for j in range(3):
            if input[i][j] == ' ':
                input[i][j] = player
                score = minimax(input, False, player)
                input[i][j] = ' '
                if score > bestScore:
                    bestScore = score
                    move = [i, j]
                # print(f"{i}, {j} - {score}")
    return move


def minimax(input, maximizing, player):
    w = checkW(input)

    if w == player:
        # print(input)
        return 1
    elif w == 'tie':
        # print(input)
        return 0
    elif w != player and w != ' ':
        # print(input)
        return -1

    if maximizing:
        turn = player
    else:
        if player == "x":
            turn = "o"
        else:
            turn = "x"

    scores = []

    for i in range(0, 3):
        for j in range(0, 3):
            if input[i][j] == " ":
                input[i][j] = turn
                scores.append(minimax(input, not maximizing, player))
                input[i][j] = " "

    return max(scores) if maximizing else min(scores)


def run():
    client.run('TOKEN')


run()
