use std::hash::Hash;
use std::{fs::File, io::Read};

use std::collections::HashSet;

pub fn run_puzzle(puzzle: u8, input: File) {
    match puzzle {
        1 => puzzle_1(input),
        2 => puzzle_2(input),
        other => panic!("Unknown puzzle number: {}", other),
    }
}

fn read_input(input: &mut File) -> String {
    let mut content = String::new();
    match input.read_to_string(&mut content) {
        Ok(_) => return content,
        Err(e) => panic!("Couldn't read the input: {}", e),
    }
}

struct Point {
    row: usize,
    col: usize,
}

impl Point {
    pub fn from(row: usize, col: usize) -> Self {
        Point { row, col }
    }
}

impl PartialEq for Point {
    fn eq(&self, other: &Self) -> bool {
        self.row == other.row && self.col == other.col
    }
}

impl Eq for Point {}

impl Hash for Point {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.row.hash(state);
        self.col.hash(state);
    }
}

fn get_forest_info(forest: String) -> (HashSet<Point>, Point) {
    let mut trees = HashSet::<Point>::new();
    
    let mut max_row = 0;
    let mut max_col = 0;

    for (row, line) in forest.lines().enumerate() {
        max_row = row;
        for (col, c) in line.chars().enumerate() {
            max_col = col;
            if c == '#' {
                trees.insert(Point::from(row, col));
            }
        }
    }

    let size = Point::from(max_row + 1, max_col + 1);

    (trees, size)
}

fn count_encountered_trees(trees: &HashSet<Point>, size: &Point, pattern: Point) -> u32 {
    let mut encountered_trees: u32 = 0;

    let mut position = Point {row: 0, col: 0};
    while position.row <= size.row {
        position.row += pattern.row;
        position.col = (pattern.col + position.col) % size.col;

        if trees.contains(&position) {
            encountered_trees += 1;
        }
    }

    encountered_trees
}

fn puzzle_1(mut input: File) {
    let forest = read_input(&mut input);
    let (trees, size) = get_forest_info(forest);

    let encountered_trees = count_encountered_trees(&trees, &size, Point::from(1, 3));

    println!("Trees encountered: {}", encountered_trees);
}

fn puzzle_2(mut input: File) {
    let forest = read_input(&mut input);
    let (trees, size) = get_forest_info(forest);

    let patterns = vec![
        Point::from(1, 1),
        Point::from(1, 3),
        Point::from(1, 5),
        Point::from(1, 7),
        Point::from(2, 1),
    ];

    let mut encountered_trees = 1; // neutral value for product

    for pattern in patterns {
        encountered_trees *= count_encountered_trees(&trees, &size, pattern);
    }

    println!("Trees encountered: {}", encountered_trees);
}