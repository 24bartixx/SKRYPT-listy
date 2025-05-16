from classes.series_validators import *
from other.get_time_series import get_time_series_transpose


def print_result(validator_name, result):
    
    print(f"\n===== {validator_name} ({len(result)}) =====")
    
    i = 0
    while i < len(result) and i < 3:
        print(f"\t{result[i]}")
        i += 1
        
    if i < len(result):
        print("\t...")


def validators_tests(path = "data/measurements/2023_NO_1g.csv"):
    
    file_time_series = get_time_series_transpose(path)[0]
    
    validators = [
        OutlierDetector(5),
        ThresholdDetector(1.6),
        ZeroSpikeDetector(),
        SimpleValidator()
    ]
    
    for validator in validators:
        print_result(validator.__class__.__name__, validator.analyze(file_time_series))
    print()
    
    print(validators[:-1])
    
    composite_or = CompositeValidator(validators[:-1], CompositeValidator.MODE.OR)
    print_result(composite_or.__class__.__name__ + " (OR)", composite_or.analyze(file_time_series))
    
    composite_and = CompositeValidator(validators[:-2], CompositeValidator.MODE.AND)
    print_result(composite_and.__class__.__name__ + " (AND)", composite_and.analyze(file_time_series))
    
    
if __name__ == "__main__":
    validators_tests()
    