use std::{error::Error, fs::File, io::Read};
use std::option::Option::{Some, None};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day4.txt")?;
    
    // solve both parts
    part_1(&input);
    part_2(&input);

    Ok(())
}

fn read_input(file_path: &str) -> Result<String, Box<dyn Error>> {
    let mut input = File::open(file_path)?;
    
    let mut content = String::new();
    input.read_to_string(&mut content)?;
    Ok(content)
}

#[derive(Debug)]
struct Passport {
    byr: Option<String>, // Birth Year
    iyr: Option<String>, // Issue Year
    eyr: Option<String>, // Expiration Year
    hgt: Option<String>, // Height
    hcl: Option<String>, // Hair Color
    ecl: Option<String>, // Eye Color
    pid: Option<String>, // Passport ID
    cid: Option<String>, // Country ID
}

impl Passport {
    pub fn new() -> Self {
        Passport { byr: None, iyr: None, eyr: None, hgt: None, hcl: None, ecl: None, pid: None, cid: None }
    }

    pub fn has_required_fields(&self) -> bool {
        [
            &self.byr,
            &self.iyr,
            &self.eyr,
            &self.hgt,
            &self.hcl,
            &self.ecl,
            &self.pid,
        ].iter().all(|key| key.is_some())
    }

    pub fn is_valid(&self) -> bool {
        if !self.has_required_fields() {
            return false
        }
        
        // birth year: 1920 - 2002
        if let Some(birth_year) = self.byr.as_ref().and_then(|s| s.parse::<u32>().ok()) {
            if birth_year < 1920 || birth_year > 2002 {
                return false
            }
        }

        // issue year: 2010 - 2020
        if let Some(issue_year) = self.iyr.as_ref().and_then(|s| s.parse::<u32>().ok()) {
            if issue_year < 2010 || issue_year > 2020 {
                return false
            }
        }

        // expiration year: 2020 - 2030
        if let Some(expiration_year) = self.eyr.as_ref().and_then(|s| s.parse::<u32>().ok()) {
            if expiration_year < 2020 || expiration_year > 2030 {
                return false
            }
        }

        // height: 50-193 cm, 9-76 in
        if let Some((height, unit)) = self.hgt.as_ref().and_then(|s| Some(s.split_at(s.len()-2))) {
            let height = height.parse::<u32>().unwrap();

            match unit {
                "cm" => if height < 150 || height > 193 {
                    return false
                },
                "in" => if height < 9 || height > 76 {
                    return false
                },
                _ => return false,
            }
        }

        // hair color: #[hex value]
        let mut hair_color = self.hcl.as_ref().unwrap().chars();
        
        // check '#' char before hex value
        if hair_color.next().unwrap() != '#' {
            return false
        }

        // check hex value
        let hex_value: Vec<char> = hair_color.collect();

        if hex_value.len() != 6 {
            return false
        }

        for digit in hex_value {
            if !digit.is_ascii_hexdigit() {
                return false
            }
        }

        // eye color: [amb, blu, brn, gry, grn, hzl, oth]
        let eye_color = self.ecl.as_ref().unwrap().as_str();
        if !["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].contains(&eye_color) {
            return false
        }

        // passport id: 9 digits long
        let passport_id = self.pid.as_ref().unwrap();

        if !(passport_id.len() == 9 && passport_id.parse::<u32>().is_ok()) {
            return false
        }

        return true
    }
}

fn get_passport_from_raw(raw_passport: &str) -> Passport {
    let mut passport = Passport::new();

    for field in raw_passport.split_whitespace() {
        if let Some((key, value)) = field.split_once(':') {
             match key {
                "byr" => passport.byr = Some(value.to_string()),
                "iyr" => passport.iyr = Some(value.to_string()),
                "eyr" => passport.eyr = Some(value.to_string()),
                "hgt" => passport.hgt = Some(value.to_string()),
                "hcl" => passport.hcl = Some(value.to_string()),
                "ecl" => passport.ecl = Some(value.to_string()),
                "pid" => passport.pid = Some(value.to_string()),
                "cid" => passport.cid = Some(value.to_string()),
                other => println!("Unknown Passport key found: {}", other),
             }
        }
    }

    passport
}

fn get_passports_from_input(input: &String) -> Vec<Passport> {
    let mut passports = Vec::new();

    for raw_password in input.split("\n\n") {
        passports.push(get_passport_from_raw(raw_password));
    }

    passports
}

fn part_1(input: &String) {
    let passports = get_passports_from_input(input);

    let mut valid_passports = 0;

    for passport in passports {
        if passport.has_required_fields() {
            valid_passports += 1;
        }
    }

    println!("Valid passports: {}", valid_passports);
}

fn part_2(input: &String) {
    let passports = get_passports_from_input(input);

    let mut valid_passports = 0;

    for passport in passports {
        if passport.is_valid() {
            valid_passports += 1;
        }
    }

    println!("Valid passports: {}", valid_passports);
}
