use std::cmp::{min, max};
use std::collections::VecDeque;
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

    let (raw_ranges, raw_ids) = input.trim()
        .split_once("\n\n")
        .unwrap_or_else(|| ("", ""));

    let mut fresh_ranges = FreshRanges::from(&raw_ranges)?;
    let ids: Vec<u64> = raw_ids.trim()
        .split("\n")
        .map(|s| s.parse::<u64>().unwrap())
        .collect();

    println!("Fresh ingredients: {}", fresh_ranges.count_fresh_ingredients(&ids));

    fresh_ranges.simplify();
    println!("Number of possible fresh ingredients: {}", fresh_ranges.count_fresh());

    Ok(())
}

#[derive(Clone, Debug, PartialEq)]
struct Range {
    lower: u64,
    upper: u64,
}

impl Range {
    pub fn new(a: u64, b: u64) -> Self {
        match b.cmp(&a) {
            std::cmp::Ordering::Greater => Self { 
                lower: a, 
                upper: b,
            },
            _ => Self { 
                lower: b, 
                upper: a,
            },
        }
    }

    pub fn from(raw: &str) -> Result<Self, Box<dyn Error>> {
        let bounds_str = raw.split_once("-").unwrap_or_else(|| ("", ""));

        let lower = bounds_str.0.parse()?;
        let upper = bounds_str.1.parse()?;

        Ok(Self::new(lower, upper))
    }

    pub fn len(&self) -> usize {
        (self.upper - self.lower + 1) as usize
    }

    pub fn union(&self, other: &Range) -> Option<Range> {
        if self.no_overlap(other) {
            return None;
        }

        // One included in the other
        if self.is_in(other) {
            return Some(other.clone());
        }
        if other.is_in(self) {
            return Some(self.clone());
        }

        // Partial overlap
        Some(
            Range::new(
                min(self.lower, other.lower), 
                max(self.upper, other.upper),
            )
        )
    }

    fn is_in(&self, other: &Range) -> bool {
        self.lower >= other.lower && self.upper <= other.upper
    }

    fn no_overlap(&self, other: &Range) -> bool {
        self.upper < other.lower || self.lower > other.upper
    }

    pub fn in_bounds(&self, number: u64) -> bool {
        number >= self.lower && number <= self.upper
    }
}

struct FreshRanges {
    ranges: Vec<Range>,
}

impl FreshRanges {
    pub fn new(ranges: &[Range]) -> Self {
        let ranges = ranges.to_vec();

        let mut fresh_ranges = Self { ranges };
        fresh_ranges.sort();
        
        fresh_ranges
    }

    pub fn from(raw: &str) -> Result<Self, Box<dyn Error>> {
        let ranges = raw.split("\n")
            .map(|r| Range::from(r))
            .collect::<Result<Vec<_>, Box<dyn Error>>>()?;

        Ok(Self::new(&ranges))
    }

    pub fn is_fresh(&self, id: u64) -> bool {
        self.ranges.iter()
            .any(|range| range.in_bounds(id))
    }

    pub fn count_fresh_ingredients(&self, ids: &[u64]) -> usize {
        ids.iter()
            .filter(|id| self.is_fresh(**id))
            .count()
    }

    pub fn count_fresh(&self) -> usize {
        self.ranges
            .iter()
            .map(|r| r.len())
            .sum()
    }

    pub fn simplify(&mut self) {
        let mut count = self.count_fresh();
        self.one_step_simplification();

        while self.count_fresh() != count {
            count = self.count_fresh();
            self.one_step_simplification();
        }
    }

    fn one_step_simplification(&mut self) {
        let mut simplified_ranges = VecDeque::from(self.ranges.clone());

        let mut i = 0;
        while i <= simplified_ranges.len()-1 {
            let r1 = simplified_ranges.pop_front().unwrap();
            let r2 = simplified_ranges.pop_front().unwrap();

            match r1.union(&r2) {
                Some(r) => {
                    simplified_ranges.push_back(r);                
                },
                None => {
                    simplified_ranges.push_back(r1);
                    simplified_ranges.push_back(r2);
                    i += 1;
                },
            }
        }

        self.ranges = Vec::from(simplified_ranges);
        self.sort();
    }

    pub fn sort(&mut self) {
        self.ranges.sort_by_key(|r| r.lower);
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn example() {
        let input = "3-5
10-14
16-20
12-18

1
5
8
11
17
32";
        let (raw_ranges, raw_ids) = input.trim()
        .split_once("\n\n")
        .unwrap_or_else(|| ("", ""));

        let mut fresh_ranges = FreshRanges::from(&raw_ranges).unwrap();
        let ids: Vec<u64> = raw_ids.trim()
            .split("\n")
            .map(|s| s.parse::<u64>().unwrap())
            .collect();


        assert_eq!(fresh_ranges.count_fresh_ingredients(&ids), 3);

        fresh_ranges.simplify();
        assert_eq!(fresh_ranges.count_fresh(), 14);
    }

    #[test]
    fn range_union() {
        let r1 = Range::new(1, 4);
        let r2 = Range::new(2, 3);
        assert_eq!(r1.union(&r2), Some(r1));

        let r1 = Range::new(2, 3);
        let r2 = Range::new(1, 4);
        assert_eq!(r1.union(&r2), Some(r2));

        let r1 = Range::new(1, 4);
        let r2 = Range::new(3, 5);
        assert_eq!(r1.union(&r2), Some(Range::new(1, 5)));

        let r1 = Range::new(3, 5);
        let r2 = Range::new(1, 4);
        assert_eq!(r1.union(&r2), Some(Range::new(1, 5)));

        let r1 = Range::new(1, 4);
        let r2 = Range::new(5, 7);
        assert_eq!(r1.union(&r2), None);

        let r1 = Range::new(5, 7);
        let r2 = Range::new(1, 4);
        assert_eq!(r1.union(&r2), None);
    }
}