use std::collections::HashSet;
use std::env;
use std::fs::File;
use std::io::Read;
use std::error::Error;

fn get_input() -> Result<String, Box<dyn Error>> {
    let input_path = match env::args().nth(1) {
        Some(path) => path,
        None => panic!("Please specify a path for the input file."),
    };
    let mut file = File::open(input_path)?;
    let mut input = String::new();
    file.read_to_string(&mut input)?;

    Ok(input)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = get_input()?;

    let passphrases: Vec<&str> = input.trim().split("\n").collect();
    println!("Valid passphrases: {}", count_valid_passphrases(&passphrases));
    println!("Valid passphrases without anagrams: {}", count_valid_passphrases_no_anagram(&passphrases));

    Ok(())
}

fn count_valid_passphrases(passphrases: &Vec<&str>) -> u32 {
    passphrases.iter()
        .map(|p| verify_passphrase(p) as u32)
        .sum()
}

fn verify_passphrase(passphrase: &str) -> bool {
    let mut words = HashSet::new();

    for word in passphrase.split_whitespace() {
        if words.contains(word) {
            return false;
        }
        words.insert(word);
    }

    return true;
}

fn count_valid_passphrases_no_anagram(passphrases: &Vec<&str>) -> u32 {
    passphrases.iter()
        .map(|p| verify_passphrase_no_anagram(p) as u32)
        .sum()
}

fn verify_passphrase_no_anagram(passphrase: &str) -> bool {
    let mut words = HashSet::new();

    for word in passphrase.split_whitespace() {
        let mut chars: Vec<char> = word.chars().collect();
        chars.sort();

        let sorted_word: String = chars.iter().collect();

        if words.contains(&sorted_word) {
            return false;
        }
        words.insert(sorted_word);
    }

    return true;
}