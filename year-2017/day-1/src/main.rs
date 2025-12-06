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

    println!("Simple captcha: {}", compute_captcha(&input, 1));
    println!("Halfway captcha: {}", compute_captcha(&input, input.len() / 2));

    Ok(())
}

fn compute_captcha(sequence: &str, step: usize) -> u32 {
    let mut sum = 0;
    let digits: Vec<char> = sequence.trim().chars().collect();

    for idx in 0..digits.len() {
        if digits[idx] == digits[(idx + step) % digits.len()] {
            let value = digits[idx].to_digit(10).unwrap();
            sum += value;
        }
    }

    sum
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn compute_simple_captcha() {
        assert_eq!(compute_captcha("1122", 1), 3);
        assert_eq!(compute_captcha("1111", 1), 4);
        assert_eq!(compute_captcha("1234", 1), 0);
        assert_eq!(compute_captcha("91212129", 1), 9);
    }

    #[test]
    fn compute_halfway_captcha() {
        assert_eq!(compute_captcha("1212", "1212".len() / 2), 6);
        assert_eq!(compute_captcha("1221", "1221".len() / 2), 0);
        assert_eq!(compute_captcha("123425", "123425".len() / 2), 4);
        assert_eq!(compute_captcha("123123", "123123".len() / 2), 12);
        assert_eq!(compute_captcha("12131415", "12131415".len() / 2), 4);
    }
}
