import os

def check_valid(passport, valid=False):
    # Missing cid is fine
    EXPECTED_FIELDS = ["byr", "iyr", "eyr", "hgt", 
                       "hcl", "ecl", "pid", "cid"]

    valid = all(field in passport for field in EXPECTED_FIELDS[:-1])

    return valid

def check_bounds(value, bounds):
    return bounds[0] <= int(value) <= bounds[1]

def check_height(value):
    if value[-2:] == "cm" and check_bounds(value[:-2], [150, 193]):
        return True
    elif value[-2:] == "in" and check_bounds(value[:-2], [59, 76]):
        return True
    else:
        return False

def check_fields(passport):
    EXPECTED_ECL = ["amb", "blu", "brn", "gry", 
                    "grn", "hzl", "oth"]

    check_condition = {
        "byr": lambda val: check_bounds(val, [1920, 2002]),
        "iyr": lambda val: check_bounds(val, [2010, 2020]),
        "eyr": lambda val: check_bounds(val, [2020, 2030]),
        "hcl": lambda val: val[0] == "#" and val[1:].isalnum() and len(val[1:]) == 6,
        "hgt": lambda val: check_height(val),
        "ecl": lambda val: val in EXPECTED_ECL,
        "pid": lambda val: val.isnumeric() and len(val) == 9,
        "cid": lambda val: True
    }

    if not check_valid(passport):
        return False
    else:
        field_pairs = passport.split()
        field_pairs = [f.split(":") for f in field_pairs]

        for key, value in field_pairs:
            if not check_condition[key](value):
                return False       
        return True
    
    
if __name__ == "__main__":
    # User input 
    passport_file = input("Enter path to batch of passports: ")

    # Read passport batch
    with open(os.path.realpath(passport_file), "r") as f:
        passport_batch = f.read()

    # Separate passports by empty line
    passports = passport_batch.rsplit("\n\n")
    passports = [passport.replace("\n", " ") for passport in passports]

    #   Check passport
    valid_1, valid_2 = 0, 0
    for passport in passports:
        valid_1 += check_valid(passport)
        valid_2 += check_fields(passport)

    # Answers
    print("Number of valid passports: {}".format(valid_1))
    print("Number of valid passports with valid fields: {}".format(valid_2))

