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

    let mut grid = Grid::new(&input);

    println!("Accessible rolls: {}", grid.accessible_rolls().len());
    println!("Removable rolls: {}", grid.removable_rolls());

    Ok(())
}

struct Grid {
    rolls: HashSet<(i32, i32)>,
    size: (usize, usize),
}

impl Grid {
    pub fn new(map: &str) -> Self {
        let lines: Vec<(usize, &str)> = map.trim().split("\n").enumerate().collect();

        let mut rolls = HashSet::new();
        let size = (lines.len(), lines[0].1.len());

        for (x, line) in lines {
            for (y, char) in line.trim().split("").enumerate() {
                if char == "@" {
                    rolls.insert((x as i32, y as i32));
                }
            }
        }

        Self { 
            rolls,
            size,
        }
    }

    pub fn count_neighbors(&self, position: (i32, i32)) -> u32 {
        let mut neighbors = 0;
        let (x0, y0) = position;

        for x in x0-1..x0+2 {
            for y in y0-1..y0+2 {
                if x == x0 && y == y0 {
                    continue;
                }

                if self.rolls.contains(&(x, y)) {
                    neighbors += 1;
                }   
            }
        }

        neighbors
    }

    pub fn accessible_rolls(&self) -> HashSet<(i32, i32)> {
        let mut accessible_rolls = HashSet::new();

        for roll in self.rolls.iter() {
            if self.count_neighbors(roll.clone()) < 4 {
                accessible_rolls.insert(*roll);
            }
        }

        accessible_rolls
    }

    pub fn removable_rolls(&mut self) -> usize {
        let mut removed_rolls = 0;

        let original_rolls = self.rolls.clone();
        let mut accessible_rolls = self.accessible_rolls();

        while !accessible_rolls.is_empty() {
            removed_rolls += accessible_rolls.len();
            self.rolls = self.rolls.difference(&accessible_rolls)
                .map(|roll| *roll)
                .collect();
            
            accessible_rolls = self.accessible_rolls();
        }

        self.rolls = original_rolls;

        removed_rolls
    }

    pub fn print(&self) {
        let mut grid = String::new();

        for x in 0..self.size.0 {
            for y in 1..self.size.1+1 {
                if self.rolls.contains(&(x as i32, y as i32)) {
                    grid += "@";
                } else {
                    grid += ".";
                }
            }

            grid += "\n";
        }

        print!("{}", grid);
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn example() {
        let input = "..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.";

        let mut grid = Grid::new(input);

        assert_eq!(grid.accessible_rolls().len(), 13);
        assert_eq!(grid.removable_rolls(), 43);
    }
}