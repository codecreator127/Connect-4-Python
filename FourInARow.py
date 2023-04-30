"""
Compsci 130 Assignment - Connect Four
Name: John Lin    UPI: jlin865   Sections: 1 - 5 of assignment
Contains a class Gameboard and a class FourInARow
Gameboard contains the all the underlying functionalities required to run the connect four game
FourInARow contains all the functions required for user interactions with the gameboard class
"""

class GameBoard:
    def __init__(self, size):
        """initializer for gameboard"""
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
    
    def num_free_positions_in_column(self, column):
        """calculates number of free positions in column"""
        free_positions = self.size
        for i in range(self.size):
            if self.items[column][i] != 0:
                free_positions -= 1
        return free_positions
        
    def game_over(self):
        """determines if all slots are full"""
        free_columns = self.size
        for i in range(self.size):
            if self.num_free_positions_in_column(i) == 0:
                free_columns -= 1
        if free_columns == 0:
            return True
        else:
            return False
            
    def display(self):
        """displays the current gameboard and scores"""
        #print out board row by row
        for row in range(self.size):
            row_output = ''
            for column in range(self.size):
                if self.items[column][self.size - row - 1] == 0:
                    row_output += '  '
                elif self.items[column][self.size - row - 1] == 1:
                    row_output += 'o '
                elif self.items[column][self.size - row - 1] == 2:
                    row_output += 'x '
            print(row_output[:-1])

        #display column numbers
        print((2 * self.size - 1) * '-')
        columns_string = ''
        for i in range(self.size):
            columns_string += str(i) + ' '
        print(columns_string[:-1])
        
        #display player points
        print('Points player 1: ' + str(self.points[0]))
        print('Points player 2: ' + str(self.points[1]))
  
    def num_new_points(self, column, row, player):
        """returns number of new points after a point is placed"""
        new_points = 0

        #calculate horizontal points gained
        #create horizontal list
        horizontal = []
        for i in range(-3, 4, 1):
            if column + i < self.size and column + i >= 0:
                horizontal.append(self.items[column + i][row])

        #check score from horizontal list
        for i in range(len(horizontal) - 3):
            if horizontal[i] == player:
                if horizontal[i + 1] == player:
                    if horizontal[i + 2] == player:
                        if horizontal[i + 3] == player:
                            new_points += 1
        
        #calculate vertical points gained
        #create vertical list
        vertical = []
        for i in range(-3, 4, 1):
            if row + i < self.size and row + i >= 0:
                vertical.append(self.items[column][row + i])

        #check score from vertical list
        for i in range(len(vertical) - 3):
            if vertical[i] == player:
                if vertical[i + 1] == player:
                    if vertical[i + 2] == player:
                        if vertical[i + 3] == player:
                            new_points += 1

        #check diagonal points gained
        #create first diagonal list
        diagonal1 = []
        for i in range(3, 0, -1):
            if column + i < self.size and row + i < self.size:
                diagonal1.append(self.items[column + i][row + i])
        for i in range(4):
            if column - i >= 0 and row - i >= 0:
                diagonal1.append(self.items[column - i][row - i])

        #check points gained from diagonal 1
        for i in range(len(diagonal1) - 3):
            if diagonal1[i] == player:
                if diagonal1[i + 1] == player:
                    if diagonal1[i + 2] == player:
                        if diagonal1[i + 3] == player:
                            new_points += 1

        #create second diagonal list
        diagonal2 = []
        for i in range(3, 0, -1):
            if column - i >= 0 and row + i < self.size:
                diagonal2.append(self.items[column - i][row + i])
        for i in range(4):
            if column + i < self.size and row - i >= 0:
                diagonal2.append(self.items[column + i][row - i])

        #check points gained from diagonal 2
        for i in range(len(diagonal2) - 3):
            if diagonal2[i] == player:
                if diagonal2[i + 1] == player:
                    if diagonal2[i + 2] == player:
                        if diagonal2[i + 3] == player:
                            new_points += 1
                            
        return new_points

    def add(self, column, player):
        """adding a new move to the board"""
        if self.num_entries[column] >= self.size:
            return False
        else:
            row = self.num_entries[column]
            
            if player == 1:
                self.items[column][row] = player
            elif player == 2:
                self.items[column][row] = player
                
            self.num_entries[column] += 1
            new = self.num_new_points(column, row, player)
            self.points[player - 1] += new

            return True

    def free_slots_as_close_to_middle_as_possible(self):
        """gives a list starting from the closest free column to the middle"""
        free_slots = []
        board_middle = (self.size - 1) / 2

        #if size is odd
        if (board_middle) % 1 == 0:
            board_middle = int(board_middle)
            if self.num_free_positions_in_column(board_middle) > 0:
                free_slots.append(board_middle)

            for i in range(1, (self.size) // 2 + 1):
                if self.num_free_positions_in_column(board_middle - i) > 0:
                    free_slots.append(int(board_middle - i))

                if self.num_free_positions_in_column(board_middle + i) > 0:
                    free_slots.append(int(board_middle + i))            
        
        #if size is even
        else:
            for i in range(self.size // 2):
                if self.num_free_positions_in_column(int(board_middle - 0.5 - i)) > 0:
                    free_slots.append(int(board_middle - 0.5 - i))

                if self.num_free_positions_in_column(int(board_middle + 0.5 + i)) > 0:
                    free_slots.append(int(board_middle + 0.5 + i))

        return free_slots

    def column_resulting_in_max_points(self, player):
        """calculates the best slot to get maximum points"""
        potential_max_points = []

        #iterates through each column
        for i in range(self.size):

            #simulates what the increase in score would be if column is played
            if self.num_entries[i] < self.size:
                self.items[i][self.num_entries[i]] = player
                
                points = self.num_new_points((i), self.num_entries[i], player)
                self.items[i][self.num_entries[i]] = 0
                
                if len(potential_max_points) == 0:
                    potential_max_points.append((i, points))
                
                if points == potential_max_points[0][1]:
                    potential_max_points.append((i, points))
                    
                elif points > potential_max_points[0][1]:
                    potential_max_points.clear()
                    potential_max_points.append((i, points))
                
        closest = self.size

        if self.size % 2 == 0:
            half = self.size // 2 - 1
        else:
            half = self.size // 2
        output = 0
        
        #if there are multiple columns resulting in the same score, find closest one to center
        if len(potential_max_points) > 1:
            for pair in potential_max_points:
                if abs(half - pair[0]) < closest:
                    closest = abs(half - pair[0])
                    output = pair
        else:
            output = potential_max_points[0]
        
        return output

class FourInARow:
    def __init__(self, size):
        self.board = GameBoard(size)

    def play(self):
        """function to play the game"""
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number = 0
        print()

        while not self.board.game_over():
            print("Player ", player_number + 1, ": ")

            if player_number == 0:

                valid_input = False
                while not valid_input:
                    
                    try:
                        column = int(input("Please input slot: "))       

                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)

                    else:
                        if column < 0 or column >= self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)

                        else:
                            if self.board.add(column, player_number + 1):
                                valid_input = True
                                
                            else:
                                print("Column ", column, "is already full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points) = self.board.column_resulting_in_max_points(2)
                if max_points > 0:
                    column=best_column

                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points) = self.board.column_resulting_in_max_points(1)
                    if max_points > 0:
                        column = best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]

                self.board.add(column, player_number + 1)
                print("The AI chooses column ", column)

            self.board.display()   
            player_number = (player_number + 1) % 2

        if (self.board.points[0] > self.board.points[1]):
            print("Player 1 (circles) wins!")

        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")

        else:  
            print("It's a draw!")

#run game here
game = FourInARow(12)
game.play()        
