import random
import time
from colorama import Fore, Style

class TicTacToe:
    def __init__(self):
        self.red_tile_num = None
        self.gamemode = "normal"
        self.player_move_turn = None
        self.difficulty = None
        self.marked_tiles = {'tile1':' ','tile2':' ','tile3':' ','tile4':' ','tile5':' ','tile6':' ','tile7':' ','tile8':' ','tile9':' '}
        self.possible_choices = [1,2,3,4,5,6,7,8,9]
        self.player_symbol = {1:"X",2:"O"}
        self.previous_moves = []
        self.winning_combinations = [
        ['tile1','tile2','tile3'],
        ['tile4','tile5','tile6'],
        ['tile7','tile8','tile9'],
        ['tile1','tile4','tile7'],
        ['tile2','tile5','tile8'],
        ['tile3','tile6','tile9'],
        ['tile1','tile5','tile9'],
        ['tile3','tile5','tile7']
    ]
    def show_board(self):
        for tile in self.marked_tiles:
            tile_num = int(tile[-1])
            symbol = self.marked_tiles[tile]

            if tile_num == self.red_tile_num:
                symbol = Fore.RED + symbol + Style.RESET_ALL

            #looks confusin but it makes the shape of the board
            if tile_num in [1,2,4,5,7,8]:
                print(f"{symbol}|",end='')
            elif tile_num in [3,6]:
                print(f"{symbol}\n-----")
            else:
                print(f"{symbol}")

    def medium_algorithm(self,player):
        for we_are in ("not blocking","blocking"):
            for tile_num in self.possible_choices:
                tile = f"tile{tile_num}"

                        #CHECK IF WE CAN WIN
                if we_are == "not blocking":
                    self.marked_tiles[tile] = self.player_symbol[player]
                           
                        #CHECK IF THIS TILE WILL BLOCK AN ENEMY WIN
                if we_are == "blocking":
                    self.marked_tiles[tile] = self.player_symbol[self.player_move_turn]
                       
                        #CHECK IF A WIN HAPPENED!
                if self.check_win_or_draw():
                    self.marked_tiles[tile] = ' '
                    return tile_num
               
                self.marked_tiles[tile]=' '
        return random.choice(self.possible_choices)            

    #This algorithm is IMPOSSIBLE to beat. It is made using a MINIMAX algorithm similar to what chess bots use!
    def impossible_algorithm(self, is_Maximising_Player, depth=0):

        count_points = self.check_win_or_draw()

        if count_points is not None:
            return (count_points * (10 - depth), None)
       
        best_score = -float("inf") if is_Maximising_Player else float("inf")
        best_move = None

        for tiles in self.marked_tiles:
            if self.marked_tiles[tiles] != ' ': 
                continue
            self.marked_tiles[tiles] = "X" if is_Maximising_Player else "O"
            score_tried = self.impossible_algorithm(not is_Maximising_Player, depth + 1)[0]

            if is_Maximising_Player:
                if score_tried > best_score:
                    best_score = score_tried
                    best_move = int(tiles[-1])
            else:
                if score_tried < best_score:
                    best_score = score_tried
                    best_move = int(tiles[-1])

            self.marked_tiles[tiles] = ' '

        return (best_score, best_move)


    def computer_turn(self,player):
        print(f"Computer's turn ({self.player_symbol[player]})!")
        time.sleep(0.5)
        if self.difficulty == "easy":
            tile_choice = random.choice(self.possible_choices)
        elif self.difficulty == "medium":
            tile_choice = self.medium_algorithm(player)
        elif self.difficulty == "impossible":
            if len(self.possible_choices) == 9:
                tile_choice = 1
            else:
                computer_sym = self.player_symbol[player]
                tile_choice = self.impossible_algorithm(True if computer_sym == 'X' else False)[1]

        print(f'Computer chooses: {tile_choice}')
        time.sleep(0.5)
        self.marktile(tile_choice, player)


       
    def player_turn(self,player):
        while True:
            print('********************')
            print(f"Player {player}' turn ({self.player_symbol[player]})")

            try:
                tile_choice = int(input('Choose a tile starting from the top left (1-9)\n'))

                if tile_choice not in self.possible_choices:
                    print('Please choose a valid vacant tile')
                    continue

                self.marktile(tile_choice, player)
         
                break
            except ValueError:
                print('Invalid Input: Please enter a valid number!')
                continue

    def marktile(self, tile_number, player):
            self.marked_tiles[f'tile{tile_number}']=self.player_symbol[player]
            self.possible_choices.remove(tile_number)
            self.previous_moves.append(tile_number)
            if self.gamemode == "infinite":
                if len(self.previous_moves) == 8:
                    revive_tile_num = self.previous_moves.pop(0)
                    self.marked_tiles[f'tile{revive_tile_num}'] = ' '
                    self.possible_choices.append(revive_tile_num)
                if len(self.previous_moves) == 7:
                    self.red_tile_num = self.previous_moves[0]
                    
                    

    def check_win_or_draw(self):
        for combination in self.winning_combinations:
            if self.marked_tiles.get(combination[0])==self.marked_tiles.get(combination[1]) and self.marked_tiles.get(combination[1]) == self.marked_tiles.get(combination[2]) and self.marked_tiles.get(combination[0])!=' ':
                return 1 if self.marked_tiles.get(combination[0]) == 'X' else -1

        for symbol in self.marked_tiles.values():
            if symbol == ' ': 
                return None
            
        return 0
    
    def play_game(self):
            game_over = False
            while not game_over:
                for player_number in range(1,3):
                    self.show_board()
                    if self.player_move_turn in [player_number, None]:
                        self.player_turn(player_number)
                    else:
                        self.computer_turn(player_number)

                    result = self.check_win_or_draw()
                    if result == 0:
                        self.show_board()
                        print("GAME OVER: DRAW")
                        game_over = True
                        break
                    elif result == 1:
                        self.red_tile_num = None
                        self.show_board()
                        print("GAME OVER: Player 1 wins!")
                        game_over = True
                        break
                    elif result == -1:
                        self.red_tile_num = None
                        self.show_board()
                        print("GAME OVER: Player 2 wins!")
                        game_over = True
                        break

def main():
    mode_list = ["infinite", "normal"]
    print("Welcome to my TicTacToe!")
    play_again = True
    while play_again:
        game = TicTacToe()        
        while True:
            single_player_or_multi = input("Would you like to play with a bot or with a friend? (bot/friend)\n").lower()
            if single_player_or_multi == "friend":
                break

            elif single_player_or_multi == "bot":
                while True:
                    diff_of_bot = input("What will be the difficulty of the bot? (easy,medium,impossible)\n").lower()
                    if diff_of_bot not in ["easy","medium","impossible"]:
                        print("Please enter one of the following listed above!")
                        continue
                    break
                while True:
                    player_move_when = input("Would you like to go first or second? (First,Second,Random)\n").lower()
                    if player_move_when not in ["first","second","random"]:
                        print("Please enter a valid choice")
                        continue
                    break
            else:
                print("Please pick one of the assigned options you gigs!!!")
                continue

            if player_move_when == "first": player_move_when = 1
            elif player_move_when == "second": player_move_when = 2
            else: player_move_when = random.randint(1,2)

            game.player_move_turn = player_move_when
            game.difficulty = diff_of_bot
            break

        while True:
            gamemode = input(f"What gamemode would you like to play: {', '.join(mode_list)}, or random?\n").lower()
            if gamemode == "random":
                gamemode = random.choice(mode_list)

            if gamemode not in mode_list:
                print("Please choose one of the options")
                continue

            print(f"You are playing mode {gamemode}")
            game.gamemode = gamemode

            break

        game.play_game()

        while True:
            ask_play_again = input("Would you like to play again? (yes,no)\n").lower()
            if ask_play_again == "yes":
                break
            elif ask_play_again == "no":
                print("Thanks for playing!")
                play_again = False
                break
            else:
                print("Please choose one of the assigned options!")
                continue
               

if __name__ == "__main__":
    main()
