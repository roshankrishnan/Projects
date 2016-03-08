"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from random import randint


GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    SumRolls = 0
    OnePresent = False
    for i in range (1, num_rolls + 1):
        NumberRolled = dice()
        if NumberRolled == 1:
            OnePresent = True
        else:
            SumRolls = SumRolls + NumberRolled
    if OnePresent:
        return 0
    else:
        return SumRolls
    # END Question 1


def is_prime(a):
    if a == 1:
        return False
    if a == 2:
        return True
    if a == 0:
        return False
    for i in range (2, a):
        if a % i == 0:
            return False
    return True

def next_prime(b):
    k = b + 1
    while True:
        if is_prime(k):
            return k
        k += 1

def get_score_for_0_roll(opponent_score):
    if opponent_score >= 10:
        Score = 1 + max(opponent_score//10, opponent_score - (opponent_score//10)*10)
    else:
        Score = opponent_score + 1
    if is_prime(Score):
        Score = next_prime(Score)
    return Score

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        if opponent_score >= 10:
            Score = 1 + max(opponent_score//10, opponent_score - (opponent_score//10)*10)
        else:
            Score = opponent_score + 1
    else:
        Score = roll_dice(num_rolls, dice)
    if is_prime(Score):
        return next_prime(Score)
    else:
        return Score
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score)%7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def give_ones_digit(a):
    first_digit = a % 10
    return first_digit

def give_tens_digit(b):
    tens_digit = (b % 100 - b % 10)//10
    return tens_digit

def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    a, b = give_ones_digit(score0), give_tens_digit(score0)
    c, d = give_ones_digit(score1), give_tens_digit(score1)
    if a == d and b == c:
        return True
    else:
        return False

    # END Question 4



def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    if goal == None:
        goal = 100
    while score0 <= goal and score1 <= goal:


        roll0 = take_turn(strategy0(score0, score1), score1, dice=select_dice(score0, score1))
        amount_rolls0 = strategy0(score0, score1)
        if roll0 == 0:
            score1 = score1 + amount_rolls0
        score0 = score0 + roll0
        if is_swap(score0, score1):
            temp_storage = score0
            score0 = score1
            score1 = temp_storage
        if score0 >= goal or score1 >= goal:
            break


        roll1 = take_turn(strategy1(score1, score0), score0, dice=select_dice(score1, score0))
        amount_rolls1 = strategy1(score1, score0)
        if roll1 == 0:
            score0 = score0 + amount_rolls1
        score1 = score1 + roll1
        if is_swap(score1, score0):
            temp_storage = score1
            score1 = score0
            score0 = temp_storage
        if score1 >= goal or score0 >= goal:
            break
    # END Question 5
    return score0, score1



#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.
    
    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def avgfn(*args):
        sum_here = 0
        for i in range(1, num_samples + 1):
            sum_here = sum_here + fn(*args)
        return sum_here / num_samples
    return avgfn

    # END Question 6


        

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    def get_interation(dice):
        current_maximum = 0
        for i in range(1, 11):
            current_roll = roll_dice(i, dice)
            if i == 1 and current_roll == 0:
                return 1
            if current_roll > current_maximum:
                current_maximum = current_roll
                good_num_to_roll = i
        return good_num_to_roll

    best_number = make_averaged(get_interation, num_samples)(dice)
    return round(best_number)
    
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies


def bacon_strategy(score, opponent_score, margin=7, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    Score = get_score_for_0_roll(opponent_score)
    if Score >= margin:
        return 0
    else:
        return num_rolls
      # Replace this statement
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    Score = get_score_for_0_roll(opponent_score)
    SwapScore = Score + score
    if is_swap(SwapScore, opponent_score) and SwapScore < opponent_score:
        return 0
    else:
        return num_rolls
    # END Question 9

def roll_dice_test(num_rolls, dice=six_sided):
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
   
    total_sum, j, roll_total = 0, 1, 0
    for i in range (1, 10000):
        while j <= num_rolls:
            number_rolled = randint(1,6) 
            if number_rolled == 1:
                total_sum = 0
                roll_total-= number_rolled
            roll_total += number_rolled
            j += 1
        if is_prime(roll_total) == True:
            total_sum = total_sum + next_prime(roll_total)
        else:
            total_sum += roll_total

    print (total_sum / 10000)

def get_to_100(dice, num_rolls):
    '''
    This function is meant to find an optimal amount to roll each turn and to find the average
    score per turn so that we may base our margin on it.

    After running these tests on all the possible num_rolls, we concluded that rolling a 5
    optimizes the amount of rolls it takes to get to 100. And with this info, we also concluded
    that by following this strategy we will get an average of 7.3 points per turn and thus 
    we have have something to base our margin off of for the other strategy function.
    '''
    SumRolls = 0
    TimesPlayed = 0
    for i in range (1, 1000):
        Score = 0
        HowManyRolls = 0
        num_rolls_here = num_rolls
        dice_here = dice
        while True:
            current_roll = roll_dice(num_rolls_here, dice_here)
            if is_prime(current_roll) == True:
                current_roll = next_prime(current_roll)
            if is_prime(Score):
                Score = next_prime(Score)
            Score = Score + current_roll
            HowManyRolls += 1
            if Score >= 100:
                break
        SumRolls = SumRolls + HowManyRolls
        TimesPlayed += 1
    return SumRolls/TimesPlayed
'''
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    As the margin for an average roll is about 7.3, we need to score more than this margin
    in order to beat the computer. 
    """
    # BEGIN Question 10

    if score < 100:
        num_rolls = 4
    if opponent_score - score > 20:
        num_rolls = 6
    if opponent_score - score > 40:
        num_rolls = 8
    if score - opponent_score > 20:
        num_rolls = 3
    if score - opponent_score > 40:
        num_rolls = 2
    if 100 - score < 20:
        num_rolls = 2

    if bacon_strategy(score, opponent_score, margin = 6, num_rolls = 5) == 0:
        num_rolls = 0
    
    if swap_strategy(score, opponent_score, num_rolls) == 0:
        num_rolls = 0



    return num_rolls  # Replace this statement
    # END Question 10
'''

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    As the margin for an average roll is about 7.3, we need to score more than this margin
    in order to beat the computer. 
    """
    # BEGIN Question 10

    if score < 100:
        num_rolls = 4
    if opponent_score - score > 21:
        num_rolls = 6
    if opponent_score - score > 49:
        num_rolls = 10
    if score - opponent_score > 21:
        num_rolls = 2
    if score - opponent_score > 49:
        num_rolls = 2
    if 100 - score < 20:
        num_rolls = 4
    if 100 - score < 10:
        num_rolls = 4


    if bacon_strategy(score, opponent_score, margin = 6, num_rolls = 4) == 0:
        num_rolls = 0

    worth_to_roll_zero = 1 + max(give_ones_digit(opponent_score), give_tens_digit(opponent_score)) + score

    if is_swap(worth_to_roll_zero, opponent_score) and worth_to_roll_zero < opponent_score:
        num_rolls = 0

    if 100 - score <= get_score_for_0_roll(opponent_score):
        num_rolls = 0

    if is_swap(get_score_for_0_roll(opponent_score) + score, opponent_score) and worth_to_roll_zero > opponent_score:
        num_rolls = 4

    return num_rolls  # Replace this statement


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
