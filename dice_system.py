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
    if base_roll >= 96:
        return "Critical Success!", "You have successfully completed the action with unexpected benefits."
    elif base_roll <= 5:
        return "Critical Failure!", "The action failed and led to severe consequences."
    elif final_roll >= 80:
        return "Great Success", "The action was very successful with extra benefits."
    elif final_roll >= 50:
        return "Success", "The action succeeded with some benefits."
    elif final_roll <= 20:
        return "Great Failure", "The action failed with major negative consequences."
    else:
        return "Failure", "The action failed with minor negative consequences."

# Resolve the action using luck, difficulty modifiers, and situational modifiers
def resolve_action(luck, difficulty_modifiers, situational_modifiers):
    base_roll = roll_dice()

    # 初始化修正值變數，避免未定義錯誤
    luck_modifier = 0
    total_difficulty_modifier = 0
    total_situational_modifier = 0
    total_modifier = 0

    # 判斷是否為極限成功或失敗
    if base_roll >= 96 or base_roll <= 5:
        final_roll = base_roll
    else:
        # 計算修正值
        luck_modifier, total_difficulty_modifier, total_situational_modifier = calculate_modifiers(
            luck, difficulty_modifiers, situational_modifiers
        )
        total_modifier = luck_modifier + total_difficulty_modifier + total_situational_modifier
        final_roll = base_roll + total_modifier
        final_roll = max(1, min(100, final_roll))

    # 獲取結果
    outcome, description = get_outcome(base_roll, final_roll)

    # 返回所有細節，包括修正值
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
