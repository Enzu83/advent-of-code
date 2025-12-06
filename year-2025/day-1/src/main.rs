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

    let instructions: Vec<&str> = input.trim().split("\n").collect();
    let mut dial = Dial::new();
    dial.init();
    dial.execute_instructions(&instructions)?;

    println!("Pointed at zero: {}", dial.pointed_zero);
    println!("Passed zero: {}", dial.passed_zero);

    Ok(())
}

struct Dial {
    position: i32,
    pointed_zero: i32,
    passed_zero: i32,
}

impl Dial {
    pub fn new() -> Self {
        Self{
            position: 0,
            pointed_zero: 0,
            passed_zero: 0,
        }
    }

    pub fn init(&mut self) {
        self.position = 50;
        self.pointed_zero = 0;
        self.passed_zero = 0;
    }

    fn decode_instruction(&self, instruction: &str) -> Result<i32, Box<dyn Error>> {
        let (direction, value_str) = instruction.split_at(1);
        let value = value_str.parse::<i32>()?;

        match direction {
            "L" => Ok(-value),
            "R" => Ok(value),
            other => Err(format!("Unknown rotation direction: {other}.").into())
        }
    }

    pub fn rotate(&mut self, instruction: &str) -> Result<(), Box<dyn Error>>{
        let mut rotation = self.decode_instruction(instruction)?;

        if rotation.abs() >= 100 {
            println!("{}, {}, {}", rotation, rotation % 100, (rotation / 100).abs());
        }
        // handle 360 rotation
        if rotation.abs() >= 100 {
            let full_rotations = (rotation / 100).abs();
            self.passed_zero += full_rotations;

            rotation %= 100; // remaining rotation that will change the final position of the dial
        }

        self.position += rotation; // apply rotation

        // check if the dial passed 0
        if self.position <= 0 || self.position >= 100 {
            self.passed_zero += 1;
        }

        self.position = self.position.rem_euclid(100); // keep the position in the [0, 99]

        // check if the dial stopped at 0
        if self.position == 0 {
            self.pointed_zero += 1;
        }

        Ok(())
    }

    pub fn execute_instructions(&mut self, instructions: &Vec<&str>) -> Result<(), Box<dyn Error>> {
        for instruction in instructions {
            self.rotate(instruction)?;
        }

        Ok(())
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    pub fn position_after_rotation() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();

        dial.rotate("R45")?;
        assert_eq!(dial.position, 95);

        dial.rotate("R45")?;
        assert_eq!(dial.position, 40);

        dial.rotate("L20")?;
        assert_eq!(dial.position, 20);

        dial.rotate("L45")?;
        assert_eq!(dial.position, 75);

        Ok(())
    }

    #[test]
    pub fn below_zero() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();
        dial.rotate("L65")?;

        assert_eq!(dial.passed_zero, 1);
        assert_eq!(dial.pointed_zero, 0);
        Ok(())
    }

    #[test]
    pub fn above_zero() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();
        dial.rotate("R65")?;

        assert_eq!(dial.passed_zero, 1);
        assert_eq!(dial.pointed_zero, 0);

        Ok(())
    }

    #[test]
    pub fn at_zero() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();
        dial.rotate("R50")?;

        assert_eq!(dial.passed_zero, 1);
        assert_eq!(dial.pointed_zero, 1);

        dial.init();
        dial.rotate("L50")?;

        assert_eq!(dial.passed_zero, 1);
        assert_eq!(dial.pointed_zero, 1);

        Ok(())
    }

    #[test]
    pub fn multiple_rotations() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();
        dial.rotate("R150")?;

        assert_eq!(dial.passed_zero, 2);
        assert_eq!(dial.pointed_zero, 1);

        dial.rotate("L240")?;

        assert_eq!(dial.passed_zero, 4);
        assert_eq!(dial.pointed_zero, 1);

        dial.rotate("R40")?;

        assert_eq!(dial.passed_zero, 5);
        assert_eq!(dial.pointed_zero, 2);

        Ok(())
    }

    #[test]
    pub fn rotation_from_zero() -> Result<(), Box<dyn Error>> {
        let mut dial = Dial::new();
        dial.position = 0;

        dial.rotate("R150")?;

        assert_eq!(dial.passed_zero, 1);
        assert_eq!(dial.pointed_zero, 0);

        dial.rotate("L250")?;

        assert_eq!(dial.passed_zero, 4);
        assert_eq!(dial.pointed_zero, 1);

        dial.rotate("L200")?;

        assert_eq!(dial.passed_zero, 6);
        assert_eq!(dial.pointed_zero, 2);

        Ok(())
    }
}