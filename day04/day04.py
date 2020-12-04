import os

def check_valid(passport, valid=False):
    # Missing cid is fine
    EXPECTED_FIELDS = ["byr", "iyr", "eyr", "hgt", 
                       "hcl", "ecl", "pid", "cid"]

    valid = all(field in passport for field in EXPECTED_FIELDS[:-1])

    return valid

def check_fields(passport):
    EXPECTED_ECL = ["amb", "blu", "brn", "gry", 
                    "grn", "hzl", "oth"]

    if not check_valid(passport):
        return False
    else:
        field_pairs = passport.split()
        field_pairs = [f.split(":") for f in field_pairs]

        for key, val in field_pairs:
            if key == "byr" and (not (1920 <= int(val) <= 2002) or not (len(val) == 4)):
                return False
            elif key == "iyr" and (not (2010 <= int(val) <= 2020) or not (len(val) == 4)):
                return False
            elif key == "eyr" and (not (2020 <= int(val) <= 2030) or not (len(val) == 4)):
                return False
            elif key == "hgt":
                if not (val[-2:] == "cm" or val[-2:] == "in"):
                    return False
                elif val[-2:] == "cm" and not (150 <= int(val[:-2]) <= 193):
                    return False
                elif val[-2:] == "in" and not (59 <= int(val[:-2]) <= 76):
                    return False
            elif key == "hcl":
                if not val[0] == "#" or not (len(val[1:]) == 6 and val[1:].isalnum()):
                    return False
            elif key == "ecl":
                if val not in EXPECTED_ECL:
                    return False
            elif key == "pid":
                if not len(val) == 9:
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

