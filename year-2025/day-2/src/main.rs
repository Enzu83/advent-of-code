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

    let ranges = get_ranges(&input)?;

    let invalid_ids_sum: u64 = ranges
        .iter()
        .map(|r| r.invalid_ids(false).iter().sum::<u64>())
        .sum();

    println!("Sum of the invalid IDs (Twice): {}", invalid_ids_sum);

    let invalid_ids_sum: u64 = ranges
        .iter()
        .map(|r| r.invalid_ids(true).iter().sum::<u64>())
        .sum();

    println!("Sum of the invalid IDs (At least twice): {}", invalid_ids_sum);

    Ok(())
}

struct Range {
    lower: u64,
    upper: u64,
}

impl Range {
    pub fn new(lower: u64, upper: u64) -> Self {
        Self { lower, upper }
    }

    pub fn from_interval(interval: &str) -> Result<Self, Box<dyn Error>> {
        let (lower, upper) = interval.split_once("-").unwrap();

        Ok(Self {
            lower: lower.parse()?,
            upper: upper.parse()?,
        })
    }

    pub fn invalid_ids(&self, at_least_twice: bool) -> HashSet<u64> {
        let mut invalid_ids = HashSet::new();

        for id in self.lower..self.upper+1 {
            if match at_least_twice {
                false => self.is_invalid(id),
                true => self.is_invalid_at_least_twice(id),
            } {
                invalid_ids.insert(id);
            }
        }

        invalid_ids
    }

    fn is_invalid(&self, number: u64) -> bool {
        let string = number.to_string();

        // strings will odd lengths can be invalid
        if string.len() % 2 == 1 {
            return false;
        }

        for i in 1..(string.len() / 2) + 1 {
            if &string[..i] == &string[i..] {
                return true;
            }
        }

        return false;
    }

    fn is_invalid_at_least_twice(&self, number: u64) -> bool {
        let string = number.to_string();

        for i in 1..(string.len() / 2) + 1 {
            // pattern should divide the string
            if string.len() % i != 0 {
                continue;
            }

            let mut invalid = true;

            for j in (i..string.len()).step_by(i) {
                // check if pattern is in bounds or is different
                if j + i > string.len() || &string[..i] != &string[j..j+i] {
                    invalid = false;
                    break;
                }
            }

            if invalid {
                return true;
            }
        }

        return false;
    }

    pub fn interval(&self) -> (u64, u64) {
        (self.lower, self.upper)
    }
}


fn get_ranges(raw_ranges: &str) -> Result<Vec<Range>, Box<dyn Error>> {
    raw_ranges
        .trim()
        .split(",")
        .map(|s| Range::from_interval(s))
        .collect()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn create_range() {
        let range = Range::from_interval("11-22").unwrap();
        assert_eq!(range.interval(), (11, 22));
    }

    #[test]
    fn parse_input() {
        let input = "11-22,95-115";
        let ranges = get_ranges(input).unwrap();

        assert_eq!(ranges[0].interval(), (11, 22));
        assert_eq!(ranges[1].interval(), (95, 115));
    }

    #[test]
    fn invalid_ids() {
        let range_1 = Range::new(11, 22);
        assert_eq!(range_1.invalid_ids(false), HashSet::from([11, 22]));

        let range_2 = Range::new(95, 115);
        assert_eq!(range_2.invalid_ids(false), HashSet::from([99]));

        let range_3 = Range::new(1188511880, 1188511890);
        assert_eq!(range_3.invalid_ids(false), HashSet::from([1188511885]));
    }

    #[test]
    fn invalid_ids_at_least_twice() {
        let range_1 = Range::new(11, 22);
        assert_eq!(range_1.invalid_ids(true), HashSet::from([11, 22]));

        let range_2 = Range::new(95, 115);
        assert_eq!(range_2.invalid_ids(true), HashSet::from([99, 111]));

        let range_3 = Range::new(1188511880, 1188511890);
        assert_eq!(range_3.invalid_ids(true), HashSet::from([1188511885]));
    }

    #[test]
    fn example() {
        let input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";

        let ranges = get_ranges(input).unwrap();

        let invalid_ids_sum: u64 = ranges
            .iter()
            .map(|r| r.invalid_ids(false).iter().sum::<u64>())
            .sum();

        assert_eq!(invalid_ids_sum, 1227775554);
    }
}