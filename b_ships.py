import os
from random import randint


EMPTY = True
ROWS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F':
        5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11}
HIT = ' X '
MISS = ' O '


def create_board(rows, cols):
    board = []
    for i in range(rows):
        board_row = []
        for j in range(cols):
            board_row.append(EMPTY)
        board.append(board_row)
    return board

BOARD = create_board(12, 12)
BOARD_TO_DRAW = [["   "] * 12 for x in range(12)]


class Vehicle:

    def __init__(self, symbol, size, count_in_game):
        self.symbol = symbol
        self.size = size
        self.count_in_game = count_in_game

    # def __str__(self):
    #     return self.symbol

    def __call__(self):
        return self

    def __len__(self):
        return self.size * self.count_in_game


class Tank(Vehicle):

    def __init__(self):
        Vehicle.__init__(self, 'Tk', 3, 3)


class Jeep(Vehicle):

    def __init__(self):
        Vehicle.__init__(self, 'Jp', 1, 5)


class Howitzer(Vehicle):

    def __init__(self):
        Vehicle.__init__(self, 'Hr', 2, 4)


class Military_truck(Vehicle):

    def __init__(self):
        Vehicle.__init__(self, 'Mt', 4, 2)


VEHICLES = [Tank(), Jeep(), Howitzer(), Military_truck()]


class Game:

    def __init__(self, vehicles=[]):
        self.vehicles = vehicles

    def clear(self):
        os.system('clear')

    def valid_position(self, row, col, orientation, vehicle):
        valid = True
        if orientation == 'vertical' and row + vehicle.size >= len(BOARD):
            valid = False
        elif orientation == 'horizontal' and col + vehicle.size >= len(BOARD[0]):
            valid = False
        else:
            if orientation == 'vertical':
                for position in range(vehicle.size):
                    if BOARD[row + position][col] != EMPTY:
                        valid = False
            elif orientation == 'horizontal':
                for position in range(vehicle.size):
                    if BOARD[row][col + position] != EMPTY:
                        valid = False
        return valid

    def count_of_vehicles_in_board(self):
        total_vehicle_objects = 0
        for row in range(len(BOARD)):
            for col in range(len(BOARD[0])):
                if isinstance(BOARD[row][col], Vehicle):
                    total_vehicle_objects += 1
        return total_vehicle_objects

    def place_vehicle(self, row, col, orientation, vehicle):

        if orientation == 'vertical':
            for size in range(vehicle.size):
                BOARD[row + size][col] = vehicle
        elif orientation == 'horizontal':
            for size in range(vehicle.size):
                BOARD[row][col + size] = vehicle
        return BOARD

    def random_row(self):
        random_row = randint(0, len(BOARD) - 1)
        return random_row

    def random_col(self):
        random_col = randint(0, len(BOARD[0]) - 1)
        return random_col

    def random_orientation(self):
        random_orientation = randint(0, 1)
        if random_orientation == 0:
            orientation = 'vertical'
        else:
            orientation = 'horizontal'
        return orientation

    def spawn_all_vehicles(self):

        curent_vehicles = self.count_of_vehicles_in_board()

        for vehicle in self.vehicles:

            needed_vehicles = len(vehicle) + curent_vehicles  # 9, 5, 8, 8

            while needed_vehicles > curent_vehicles:
                random_row = self.random_row()
                random_col = self.random_col()
                random_orientation = self.random_orientation()

                if self.valid_position(random_row, random_col, random_orientation, vehicle):
                    self.place_vehicle(
                        random_row, random_col, random_orientation, vehicle)
                curent_vehicles = self.count_of_vehicles_in_board()

    def reveal_board(self, board):
        for row in range(len(board)):
            for col in range(len(board[0])):
                if isinstance(board[row][col], Vehicle):
                    print("" + board[row][col].symbol + "|", end='')
                else:
                    print("  " + "|", end='')
            print()
        return self.clear

    def player_choice(self):

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        print('You can enter A-L for row.Small letters are also possibility')
        print('You can enter 1-12 for column. 01; 02; 03 ... 09 is also possible choice :)')
        player_input = input(
            'Въведи координати, батка!' + "\n" + 'Give a shot: ')

        if len(player_input) < 2 or len(player_input) > 3:
            print(
                'Invalid input! You need to enter exactly 2 entries! ДИМИЕК, ни са прай, оу, Мари Ханън!')
            return self.player_choice()
        elif len(player_input) == 2:
            player_input = player_input + " "

        player_row = player_input[0].upper()
        player_column = player_input[1] + player_input[2]

        if is_number(player_column):
            player_column = int(player_column) - 1
        else:
            print('Enter number for column please!')
            return self.player_choice()
        if player_row not in ROWS:
            print('Invalid row')
            return self.player_choice()
        elif player_column > 12 or player_column < 0:
            print('Ivalid column.That is out of range')
            return self.player_choice()
        else:
            player_choice = {
                'player_row': ROWS[player_row], 'player_column': player_column}
            return player_choice

    def get_vehicles_position(self):
        occupied_positions = []
        for row in range(len(BOARD)):
            for col in range(len(BOARD[0])):
                if isinstance(BOARD[row][col], Vehicle):
                    occupied_positions.append([row, col])
        return occupied_positions

    def draw_board(self, board):
        print("\n" * 5)
        print(" " * 3, end='')
        for i in range(len(board)):
            print(" " + str(i + 1) + "  ", end='')
        print()
        for row in range(len(board)):
            print(" " + chr(65 + row) + "|", end='')
            for col in range(len(board[0])):
                print("" + board[row][col] + "|", end='')
            print()
        print("\n" * 5)
        return self.clear

    def play(self):

        bombed_positions = []
        count_of_alive_vehicles = self.count_of_vehicles_in_board()

        self.draw_board(BOARD_TO_DRAW)

        while count_of_alive_vehicles > 0:

            player_coordinates = self.player_choice()

            if [player_coordinates['player_row'], player_coordinates['player_column']] in bombed_positions:
                print(
                    "Those coordinates were already bombed. Please strike again somewhere else.")
                continue
            else:
                bombed_positions.append(
                    [player_coordinates['player_row'], player_coordinates['player_column']])

            if BOARD[player_coordinates['player_row']][player_coordinates['player_column']] == EMPTY:
                message = 'You missed.Shoot again'
                BOARD_TO_DRAW[player_coordinates['player_row']][
                    player_coordinates['player_column']] = MISS
            elif isinstance(BOARD[player_coordinates['player_row']][player_coordinates['player_column']], Vehicle):
                count_of_alive_vehicles -= 1
                message = 'You hit an enemy ' + BOARD[player_coordinates['player_row']][
                    player_coordinates['player_column']].__class__.__name__
                BOARD_TO_DRAW[player_coordinates['player_row']][
                    player_coordinates['player_column']] = HIT

            print(message)
            self.draw_board(BOARD_TO_DRAW)

        if count_of_alive_vehicles == 0:

            self.clear()
            print('GAME OVER!')
            print(
                'Sorry for the long lanes. I know they are in violation with pep8.')


game = Game(VEHICLES)
game.spawn_all_vehicles()


def start():
    reveal_or_no = input('Check board before game ?!? --- enter Y/N ' + "\n")

    if reveal_or_no.upper() == 'Y':
        game.reveal_board(BOARD)
        return start()
    elif reveal_or_no.upper() == 'N':
        game.play()
    else:
        return start()

start()
