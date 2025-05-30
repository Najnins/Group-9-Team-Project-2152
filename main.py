# Import the random library to use for the dice later
import random

# Put all the functions into another file and import them
import function

# Game Flow
# Define two Dice
small_dice_options = list(range(1, 7))  # Max combat strength is 6
big_dice_options = list(range(1, 21))  # Max health points is 20

# Define the number of stars to award the player
num_stars = 0
input_valid = False

# move counter to track number of moves, zone check and hp lost while using
move_count = 0
zone_active = False
zone_hp_cost = 5

# Loop to get valid input for Hero Combat Strength
i = 0
while not input_valid and i in range(5):
    combat_strength = input("Enter your combat Strength (1-6): ")

    # Validate input: Check if the string inputted is numeric
    if not combat_strength.isnumeric():
        # If one of the inputs are invalid, print error message and halt
        print("One or more invalid inputs. Player needs to enter integer numbers for Combat Strength")
        i = i + 1

    # Note: Now safe to cast combat_strength to integer
    # Validate input: Check if the string inputted
    elif int(combat_strength) not in range(1, 7):
        print("Enter a valid integer between 1 and 6 only")
        i = i + 1

    else:
        input_valid = True

m_input_valid = False

while not m_input_valid and i in range(5):
    m_combat_strength = input("Enter the monster's combat Strength (1-6): ")

    # Validate input: Check if the string inputted is numeric
    if not m_combat_strength.isnumeric():
        # If one of the inputs are invalid, print error message and halt
        print("One or more invalid inputs. Monster needs to enter integer numbers for Combat Strength")
        i = i + 1

    # Note: Now safe to cast combat_strength to integer
    # Validate input: Check if the string inputted
    elif int(m_combat_strength) not in range(1, 7):
        print("Enter a valid integer between 1 and 6 only")
        i = i + 1
    else:
        m_input_valid = True

if input_valid and m_input_valid:
    # Input was valid - broke out of while loop
    combat_strength = int(combat_strength)
    m_combat_strength = int(m_combat_strength)

    # Roll for player health points
    input("Roll the dice for your health points (Press enter)")
    health_points = random.choice(big_dice_options)
    print("Player rolled " + str(health_points) + " health points")

# Roll for monster combat strength
input("Roll the dice for the monster's combat strength (Press enter)")
m_combat_strength = random.choice(small_dice_options)
print("Player rolled " + str(m_combat_strength) + " combat strength for the monster")

# Roll for monster health points
input("Roll the dice for the monster's health points (Press enter)")
m_health_points = random.choice(big_dice_options)
print("Player rolled " + str(m_health_points) + " health points for the monster")

# Define the Weapons (reintroduced from earlier code)
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]

# Roll for hero's weapon
input("Roll the dice for your weapon (Press enter)")
weapon_roll = random.choice(small_dice_options)
current_weapon = weapons[weapon_roll - 1]
print(f"The hero's weapon is {current_weapon}")

# Weakness Exploit Bonus: Define monster weaknesses
monster_weaknesses = ["Blade", "Fire", "Blunt", "Explosive"]
current_weaknesses = random.sample(monster_weaknesses, k=2)  # 2 random weaknesses
hero_items = [current_weapon]  # No belt, just weapon

# List comprehension to calculate damage bonus
damage_bonus = sum([
    1 for weakness in current_weaknesses
    if (weakness == "Blade" and "Knife" in hero_items) or
       (weakness == "Blunt" and ("Fist" in hero_items or "Club" in hero_items)) or
       (weakness == "Explosive" and ("Gun" in hero_items or "Bomb" in hero_items or "Nuclear Bomb" in hero_items)) or
       (weakness == "Fire" and ("Bomb" in hero_items or "Nuclear Bomb" in hero_items))
])

# Feedback
print(f"Monster weaknesses detected: {current_weaknesses}")
print(f"Your weapon: {current_weapon}")
print(f"Damage bonus from weaknesses: +{damage_bonus}")

# Loop while the monster and the player are alive. Call fight sequence functions
while m_health_points > 0 and health_points > 0:
    # Fight Sequence
    # Who attacks first?
    input("Roll to see who attacks first (Press Enter)")
    attack_roll = random.choice(small_dice_options)
    if not (attack_roll % 2 == 0):
        input("You strike (Press enter)")
        # Add damage_bonus to hero's attack
        total_strength = combat_strength + damage_bonus
        m_health_points = function.hero_attacks(total_strength, m_health_points)
        move_count += 1
        if m_health_points != 0:
            input("The monster strikes (Press enter)!!!")
            # Monster Attacks Back
            health_points = function.monster_attacks(m_combat_strength, health_points)

    else:
        # Monster Attacks First
        input("The Monster strikes (Press enter)")
        health_points = function.monster_attacks(m_combat_strength, health_points)
        if health_points != 0:
            input("The hero strikes!! (Press enter)")
            # Add damage_bonus to hero's attack
            total_strength = combat_strength + damage_bonus
            m_health_points = function.hero_attacks(total_strength, m_health_points)
            move_count += 1

# --- Check for Early Win (Zone Entry) ---
if m_health_points <= 0 and move_count <= 2:
    zone_active = True
    print("\n Ideal Death Gamble Activated: The Hero enters THE ZONE! ")

    zone_total_cost = 0  # Track total health used in Zone

    while health_points > zone_hp_cost:
        choice = input(f"\nYou're in the Zone! Attack with 2.5x power for -{zone_hp_cost} HP? (yes/no): ").lower()
        if choice == "yes":
            # Deduct HP cost
            health_points -= zone_hp_cost
            zone_total_cost += zone_hp_cost

            # 2.5x attack
            total_strength = int((combat_strength + damage_bonus) * 2.5)
            m_health_points = random.randint(10, 20)  # New monster challenge
            print(f"\nA NEW MONSTER emerges with {m_health_points} HP!")
            while m_health_points > 0 and health_points > 0:
                m_health_points = function.hero_attacks(total_strength, m_health_points)
                if m_health_points > 0:
                    health_points = function.monster_attacks(m_combat_strength, health_points)

            if health_points > 0:
                print(" You won the battle and regained all HP spent in Zone!")
                health_points += zone_total_cost  # Regain spent HP
            else:
                print(" You were defeated in the Zone...")
                break
        else:
            print(" You chose to exit the Zone.")
            break


# Determine winner
if m_health_points <= 0:
    winner = "Hero"
    print("Hero wins!")
else:
    winner = "Monster"
    print("Monster wins!")

# Weakness Exploit Bonus: Post-fight rewards
if winner == "Hero":
    if damage_bonus > 0:  # At least one weakness exploited
        if damage_bonus >= 2:  # Perfect exploit (both weaknesses)
            num_stars += 1
            print(f"Perfect exploit! +1 star (Total stars: {num_stars})")
            if random.random() < 0.3:  # 30% chance for a message (no belt here)
                print("You feel lucky—weakness mastery achieved!")
        else:
            print("Good exploit, but no extra reward.")
    else:
        print("No weaknesses exploited this time.")
else:
    if damage_bonus > 0:
        print(f"You exploited weaknesses but still lost. Damage bonus was: +{damage_bonus}")
    else:
        print("Monster's weaknesses went unexploited.")

# Example belt and dream level for the personality trait system
belt = ["Health Potion", "Leather Boots", "Flimsy Gloves"]

# Ask user how many dream levels they want to go down
num_dream_lvls = -1  # initialize with invalid value
while num_dream_lvls < 0 or num_dream_lvls > 3:
    try:
        num_dream_lvls = int(input("How many dream levels do you want to go down? (Enter 0-3): "))
        if num_dream_lvls < 0 or num_dream_lvls > 3:
            print("Please enter a number between 0 and 3.")
    except ValueError:
        print("Invalid input! Please enter a whole number between 0 and 3.")

# Determine and print hero personality trait
trait = function.determine_hero_trait(health_points, belt, num_dream_lvls)