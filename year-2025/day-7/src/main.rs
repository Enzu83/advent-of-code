use std::collections::{HashMap, HashSet};
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

    let manifold = Manifold::from(&input);

    let (splits, paths) = manifold.count_splits_and_paths();

    println!("Splits: {}", splits);
    println!("Paths: {}", paths);


    Ok(())
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Beam {
    head: (usize, usize),
}

impl Beam {
    pub fn new(position: (usize, usize)) -> Self {
        Self { head: position }
    }

    pub fn split(&self) -> (Beam, Beam) {
        (
            Beam::new((self.head.0 + 1, self.head.1 - 1)),
            Beam::new((self.head.0 + 1, self.head.1 + 1)),
        )
    }
}

struct Manifold {
    start: (usize, usize),
    splitters: HashSet<(usize, usize)>,
    height: usize,
}

impl Manifold {
    pub fn new(start: (usize, usize), splitters: HashSet<(usize, usize)>, height: usize) -> Self {
        Self { start, splitters, height }
    }

    pub fn from(map: &str) -> Self {
        let mut start = (0, 0);
        let mut splitters = HashSet::new();

        let lines: Vec<(usize, &str)> = map.trim().split("\n").enumerate().collect();
        let height = lines.len()-1;

        for (i, line) in lines {
            for (j, char) in line.chars().enumerate() {
                match char {
                    '^' => {
                        splitters.insert((i, j));
                    },
                    'S' => start = (i, j),
                    _ => {},
                }
            }
        }

        Manifold::new(start, splitters, height)
    }

    pub fn count_splits_and_paths(&self) -> (usize, usize) {
        let mut remaining = Vec::from([Beam::new(self.start)]);
        let mut visited = HashMap::from([(Beam::new(self.start), 1)]);

        let mut splits = 0;

        let mut height = 0;
        while height < self.height {
            // beams of the next row
            let mut next_remaining = Vec::new();

            // clear the row before moving to the next one
            for mut beam in remaining {
                if beam.head.0 == self.height {
                    continue;
                }

                let current_count = match visited.get(&beam) {
                    Some(count) => *count,
                    None => 1,
                };

                if self.splitters.contains(&beam.head) {
                    // split in 2
                    let (beam_1, beam_2) = beam.split();
                    splits += 1;

                    insert_and_count(beam_1, &mut next_remaining, &mut visited, current_count);
                    insert_and_count(beam_2, &mut next_remaining, &mut visited, current_count);
                } else {
                    // continue
                    beam.head.0 += 1;
                    insert_and_count(beam, &mut next_remaining, &mut visited, current_count);
                }
            }

            remaining = next_remaining;
            height += 1;
        }

        let paths: usize = visited
            .iter()
            .filter(|(b, _)| b.head.0 == self.height)
            .map(|(_, v)| *v)
            .sum();

        (splits, paths)
    }
}

fn insert_and_count(beam: Beam, remaining: &mut Vec<Beam>, visited: &mut HashMap<Beam, usize>, beam_count: usize) {
    match visited.get_mut(&beam) {
        Some(count) => {
            *count += beam_count;
        },
        None => {
            remaining.push(beam.clone());
            visited.insert(beam, beam_count);
        },
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn example() {
        let input = ".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............";

        let manifold = Manifold::from(input);

        let (splits, paths) = manifold.count_splits_and_paths();

        assert_eq!(splits, 21);
        assert_eq!(paths, 40);
    }
}