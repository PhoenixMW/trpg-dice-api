# dice_system.py

import random
import math

# Roll a dice (1d100)
def roll_dice():
    return random.randint(1, 100)

# Calculate modifiers, summing all applicable modifiers
def calculate_modifiers(luck, difficulty_modifiers, situational_modifiers):
    luck_modifier = math.floor((luck - 50) / 2)

    # Sum up all difficulty and situational modifiers
    total_difficulty_modifier = sum(difficulty_modifiers)
    total_situational_modifier = sum(situational_modifiers)

    return luck_modifier, total_difficulty_modifier, total_situational_modifier

# Determine the outcome based on base and final roll
def get_outcome(base_roll, final_roll):
    # 極端成功或極端失敗判斷，這些結果應有行動以外的額外影響
    if base_roll >= 96:
        return "Extreme Success!", "You have successfully completed the action with exceptional results, and unexpected benefits."
    elif base_roll <= 5:
        return "Fumble!", "The action failed catastrophically, leading to severe unintended consequences."

    # 根據最終擲骰的結果進行行動的判斷
    if final_roll >= 80:
        return "Hard Success", "The action succeeded beyond expectations, achieving the intended result with notable effectiveness."
    elif final_roll >= 50:
        return "Regular Success", "The action succeeded, accomplishing exactly what you intended without additional effects."
    elif final_roll <= 20:
        return "Hard Failure", "The action failed significantly, leading to some negative impact on the attempt."
    else:
        return "Regular Failure", "The action did not succeed, and nothing else happens."

# Resolve the action using luck, difficulty modifiers, and situational modifiers
def resolve_action(luck, difficulty_modifiers, situational_modifiers):
    base_roll = roll_dice()

    # Initialize modifiers to avoid undefined errors
    luck_modifier = 0
    total_difficulty_modifier = 0
    total_situational_modifier = 0
    total_modifier = 0

    # Check for critical success or failure
    if base_roll >= 96 or base_roll <= 5:
        final_roll = base_roll
    else:
        # Calculate modifiers
        luck_modifier, total_difficulty_modifier, total_situational_modifier = calculate_modifiers(
            luck, difficulty_modifiers, situational_modifiers
        )
        total_modifier = luck_modifier + total_difficulty_modifier + total_situational_modifier
        final_roll = base_roll + total_modifier
        final_roll = max(1, min(100, final_roll))

    # Get outcome and description
    outcome, description = get_outcome(base_roll, final_roll)

    # Return all details, including modifiers
    result = (
        f"Base roll: {base_roll}\n"
        f"Final roll: {final_roll}\n"
        f"Outcome: {outcome}\n"
        f"Description: {description}\n"
        f"--- Modifiers Breakdown ---\n"
        f"Luck modifier: {luck_modifier}\n"
        f"Total difficulty modifier: {total_difficulty_modifier}\n"
        f"Total situational modifier: {total_situational_modifier}\n"
        f"Total modifier: {total_modifier}"
    )

    return result
