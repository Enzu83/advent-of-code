use std::collections::HashMap;
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
    let targeted_data: u32 = input.trim().parse()?;

    let mut data_points = DataPoints::new(ValueMethod::INCREMENT); // compute next values by increment
    data_points.nextn(targeted_data as usize);

    let targeted_data_position = data_points.point(targeted_data).unwrap();
    println!("Distance from origin for {} for increment value method: {}", targeted_data, targeted_data_position.distance());

    let mut data_points_adjacent = DataPoints::new(ValueMethod::ADJACENT); // compute next values based on the adjacent squares
    
    while data_points_adjacent.last_data.value < targeted_data {
        data_points_adjacent.next();
    }

    println!("First value bigger than {} for adjacent value method: {}", targeted_data, data_points_adjacent.last_data.value);

    Ok(())
}

#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    pub fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    pub fn distance(&self) -> u32 {
        (self.x.abs() + self.y.abs()) as u32
    }
}

enum Direction {
    LEFT,
    UP,
    RIGHT,
    DOWN,
}

enum ValueMethod {
    INCREMENT,
    ADJACENT,
}

struct Data {
    position: Point,
    direction: Direction,
    value: u32,
}

impl Data {
    pub fn new() -> Self {
        Self {
            position: Point::new(0, 0),
            direction: Direction::RIGHT,
            value: 1,
        }
    }
}

struct DataPoints {
    value_to_point: HashMap<u32, Point>,
    point_to_value: HashMap<Point, u32>,
    last_data: Data,
    value_method: ValueMethod,
}

impl DataPoints {
    pub fn new(value_method: ValueMethod) -> Self {
        let data_point = Data::new();
        
        let mut value_to_point = HashMap::new();
        let mut point_to_value = HashMap::new();

        value_to_point.insert(data_point.value, data_point.position.clone());
        point_to_value.insert(data_point.position.clone(), data_point.value);

        Self {
            value_to_point,
            point_to_value,
            last_data: data_point,
            value_method
        }
    }

    pub fn next(&mut self) {
        match self.last_data.direction {
            Direction::RIGHT => {
                self.last_data.position.x += 1;

                // change direction if the space is empty
                if !self.point_to_value.contains_key(&Point::new(self.last_data.position.x, self.last_data.position.y + 1)) {
                    self.last_data.direction = Direction::UP;
                }
            },
            Direction::UP => {
                self.last_data.position.y += 1;

                if !self.point_to_value.contains_key(&Point::new(self.last_data.position.x - 1, self.last_data.position.y)) {
                    self.last_data.direction = Direction::LEFT;
                }
            },
            Direction::LEFT => {
                self.last_data.position.x -= 1;
                
                if !self.point_to_value.contains_key(&Point::new(self.last_data.position.x, self.last_data.position.y - 1)) {
                    self.last_data.direction = Direction::DOWN;
                }
            },
            Direction::DOWN => {
                self.last_data.position.y -= 1;
                
                if !self.point_to_value.contains_key(&Point::new(self.last_data.position.x + 1, self.last_data.position.y)) {
                    self.last_data.direction = Direction::RIGHT;
                }
            }
        }

        self.next_value();

        self.point_to_value.insert(self.last_data.position.clone(), self.last_data.value);
        self.value_to_point.insert(self.last_data.value, self.last_data.position.clone());
    }

    pub fn nextn(&mut self, repeat: usize) {
        for _ in 0..repeat {
            self.next();
        }
    }

    fn next_value(&mut self) {
        match self.value_method {
            ValueMethod::INCREMENT => self.last_data.value += 1,
            ValueMethod::ADJACENT => {
                self.last_data.value = self.get_adjacent_points_values_sum();
            }
        }
    }

    fn get_adjacent_points_values_sum(&self) -> u32 {
        let mut sum = 0;

        for i in -1..=1 {
            for j in -1..=1 {
                if i == 0 && j == 0 {
                    continue;
                }

                let point = Point::new(self.last_data.position.x + i, self.last_data.position.y + j);
                match self.value(&point) {
                    Some(value) => sum += value,
                    None => continue,
                }
            }
        }

        sum
    }

    pub fn point(&self, value: u32) -> Option<&Point> {
        self.value_to_point.get(&value)
    }

    pub fn value(&self, point: &Point) -> Option<&u32> {
        self.point_to_value.get(point)
    }
}
