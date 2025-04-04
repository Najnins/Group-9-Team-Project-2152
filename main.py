# Import the random library to use for the dice later
import random

# Put all the functions into another file and import them
import function

# Game Flow
# Define two Dice
small_dice_options = list(range(1, 7))  # Max combat strength is 6
big_dice_options = list(range(1, 21))  # Max health points is 20

# Function to get valid combat strength input
def get_valid_strength(prompt):
    for i in range(5):  # Allow up to 5 attempts
        value = input(prompt)

        # Validate input: Check if the string inputted is numeric
        if not value.isnumeric():
            print("One or more invalid inputs. Player needs to enter integer numbers for Combat Strength")
        # Validate input: Check if the integer is in range
        elif int(value) not in range(1, 7):
            print("Enter a valid integer between 1 and 6 only")
        else:
            return int(value)

    # Exceeded input attempts
    print("Too many invalid attempts. Exiting.")
    exit()

# Get valid input for Hero Combat Strength
hero_combat_strength = get_valid_strength("Enter your combat Strength (1-6): ")

# Roll for player health points
input("Roll the dice for your health points (Press Enter)")
hero_health_points = random.choice(big_dice_options)
print("Player rolled " + str(hero_health_points) + " health points")

# Roll for monster combat strength
input("Roll the dice for the monster's combat strength (Press Enter)")
monster_combat_strength = random.choice(small_dice_options)
print("Player rolled " + str(monster_combat_strength) + " combat strength for the monster")

# Roll for monster health points
input("Roll the dice for the monster's health points (Press Enter)")
monster_health_points = random.choice(big_dice_options)
print("Player rolled " + str(monster_health_points) + " health points for the monster")

# Combat loop
while monster_health_points > 0 and hero_health_points > 0:
    input("Roll to see who attacks first (Press Enter)")
    attack_roll = random.choice(small_dice_options)

    if attack_roll % 2 != 0:
        input("You strike (Press Enter)")
        monster_health_points = function.hero_attacks(hero_combat_strength, monster_health_points)
        if monster_health_points != 0:
            input("The monster strikes (Press Enter)!!!")
            hero_health_points = function.monster_attacks(monster_combat_strength, hero_health_points)
    else:
        input("The Monster strikes (Press Enter)")
        hero_health_points = function.monster_attacks(monster_combat_strength, hero_health_points)
        if hero_health_points != 0:
            input("The hero strikes!! (Press Enter)")
            monster_health_points = function.hero_attacks(hero_combat_strength, monster_health_points)

# Example belt and dream level for the personality trait system
belt = ["Health Potion", "Leather Boots", "Flimsy Gloves"]

# Ask user how many dream levels they want to go down
num_dream_levels = -1
while num_dream_levels < 0 or num_dream_levels > 3:
    try:
        num_dream_levels = int(input("How many dream levels do you want to go down? (Enter 0-3): "))
        if num_dream_levels < 0 or num_dream_levels > 3:
            print("Please enter a number between 0 and 3.")
    except ValueError:
        print("Invalid input! Please enter a whole number between 0 and 3.")

# Determine and print hero personality trait
trait = function.determine_hero_trait(hero_health_points, belt, num_dream_levels)

# Run Minilik Mystery Portal logic
portal_status = function.mystery_portal_by_minilik(hero_combat_strength, belt)
print(f"\nMystery Portal Outcome: {portal_status}")
print("🎮 Game Over. Thanks for playing!")
