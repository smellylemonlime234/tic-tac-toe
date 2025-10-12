#when I say AI I really mean algorithm :p
import random
import time
class TicTacToe:
    def __init__(self,player_move_turn=None,difficulty=None):
        self.player_move_turn = player_move_turn
        self.difficulty = difficulty
        self.marked_tiles = {'tile1':' ','tile2':' ','tile3':' ','tile4':' ','tile5':' ','tile6':' ','tile7':' ','tile8':' ','tile9':' '}
        self.possible_choices = [1,2,3,4,5,6,7,8,9]
        self.player_symbol = {1:"X",2:"O"}
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
        print(f"{self.marked_tiles['tile1']}|{self.marked_tiles['tile2']}|{self.marked_tiles['tile3']}\n"
              f'-----\n'
              f"{self.marked_tiles['tile4']}|{self.marked_tiles['tile5']}|{self.marked_tiles['tile6']}\n"
              f'-----\n'
              f"{self.marked_tiles['tile7']}|{self.marked_tiles['tile8']}|{self.marked_tiles['tile9']}")

    def medium_ai(self,player):
        for tiles in self.marked_tiles:
            if self.marked_tiles[tiles] == ' ':
                blocking = False
                for i in range(2):
                    #CHECK IF WE CAN WIN
                    if not blocking: 
                        self.marked_tiles[tiles] = self.player_symbol[player]
                    #CHECK IF THIS TILE WILL BLOCK AN ENEMY WIN
                    if blocking: 
                        self.marked_tiles[tiles] = self.player_symbol[self.player_move_turn]
                    
                    #CHECK IF A WIN HAPPENED!
                    if self.check_win_or_draw():
                        self.marked_tiles[tiles] = ' '
                        return int(tiles[-1])
            
                    blocking = True
                self.marked_tiles[tiles]=' '
        return random.choice(self.possible_choices)            

    def impossible_ai(self, is_Maximising_Player):
        count_points = self.check_win_or_draw()

        if count_points is not None:
            return (count_points, None)
        
        best_score = -float("inf") if is_Maximising_Player else float("inf")
        best_move = None

        for tiles in self.marked_tiles:
            if self.marked_tiles[tiles] != ' ': 
                continue

            self.marked_tiles[tiles] = "X" if is_Maximising_Player else "O"
            score_tried = self.impossible_ai(not is_Maximising_Player)[0]

            if is_Maximising_Player:
                if score_tried > best_score:
                    best_score = score_tried
                    best_move = int(tiles[-1])
            else:
                if score_tried < best_score:
                    best_score = score_tried
                    best_move = int(tiles[-1])

            self.marked_tiles[tiles] = " "

        return (best_score, best_move)


    def computer_turn(self,player):
        print(f"Computer's turn ({self.player_symbol[player]})!")
        time.sleep(0.5)
        if self.difficulty == "easy":
            tile_choice = random.choice(self.possible_choices)
        elif self.difficulty == "medium":
            tile_choice = self.medium_ai(player)
        elif self.difficulty == "impossible":
            print("Starting impossible AI!")
            tile_choice = self.impossible_ai(True if player == 1 else False)[1]
        print(f'Computer chooses: {tile_choice}')
        time.sleep(0.5)
        self.marked_tiles[f'tile{tile_choice}']=self.player_symbol[player]
        self.possible_choices.remove(tile_choice)        
        
    def player_turn(self,player):
        while True:
            print('********************')
            print(f"Player {player}' turn ({self.player_symbol[player]})")

            try:
                tile_choice = int(input('Choose a tile starting from the top left (1-9)\n'))

                if tile_choice not in self.possible_choices:
                    print('Please choose a valid vacant tile')
                    continue

                self.marked_tiles[f'tile{tile_choice}']=self.player_symbol[player]
                self.possible_choices.remove(tile_choice)
         
                break
            except ValueError:
                print('Invalid Input: Please enter a valid number!')
                continue

    def check_win_or_draw(self):
        for combination in self.winning_combinations:
            if self.marked_tiles.get(combination[0])==self.marked_tiles.get(combination[1]) and self.marked_tiles.get(combination[1]) == self.marked_tiles.get(combination[2]) and self.marked_tiles.get(combination[0])!=' ':
                return 1 if self.marked_tiles.get(combination[0]) == 'X' else -1

        if len(self.possible_choices) == 0: return 0
        return None
    
    def play_game(self):
        game_over = False
        while not game_over:
            for player_number in range(1,3):
                self.show_board()
                if self.player_move_turn in [player_number,None]:
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
                    self.show_board()
                    print("GAME OVER: Player 1 wins!")
                    game_over = True
                    break
                elif result == -1:
                    self.show_board()
                    print("GAME OVER: Player 2 wins!")
                    game_over = True
                    break

def main():
    print("Welcome to my TicTacToe!")
    play_again = True
    while play_again:         
        while True:
            single_player_or_multi = input("Would you like to play with a bot or with a friend? (bot/friend)\n").lower()
            if single_player_or_multi == "friend": 
                game = TicTacToe()
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
            game = TicTacToe(player_move_when,diff_of_bot)
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
