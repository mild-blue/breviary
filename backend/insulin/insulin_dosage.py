grams = float

CARBS_RATIO_NUMERATOR = 350
INSULIN_SENSIBILITY_NUMERATOR = 110


def recommended_insulin(tddi: float,
                        target_glycemia: float,
                        current_glycemia: float,
                        expected_carbohydrate_intake: grams) \
        -> float:
    dosage_carbohydrate_intake = expected_carbohydrate_intake / (CARBS_RATIO_NUMERATOR / tddi)
    dosage_target_glycemia = (current_glycemia - target_glycemia) / (INSULIN_SENSIBILITY_NUMERATOR / tddi)
    return max(dosage_carbohydrate_intake + dosage_target_glycemia, 0)


if __name__ == '__main__':
    reco = recommended_insulin(30, 8, 5, 70)
    print(reco)
