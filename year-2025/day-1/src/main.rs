use std::env;
use std::fs::File;
use std::io::Read;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input_path = env::args().nth(1).unwrap();
    let mut file = File::open(input_path)?;
    let mut input = String::new();
    file.read_to_string(&mut input)?;

    count_zeros(input.trim().split("\n").collect());

    Ok(())
}


enum Direction {
    LEFT,
    RIGHT,
}

fn decode_rotation(rotation: &str) -> (Direction, i32) {
    let (direction_letter, amount) = rotation.split_at(1);

    match direction_letter {
        "L" => (Direction::LEFT, amount.parse::<i32>().unwrap()),
        "R" => (Direction::RIGHT, amount.parse::<i32>().unwrap()),
        _ => panic!("unknown direction: {}", direction_letter),
    }
}

fn move_dial(current_position: i32, rotation: &str) -> (i32, i32) {
    let mut number_passed_zero = 0;
    let (direction, amount) = decode_rotation(rotation);

    match direction {
        Direction::LEFT => {
            let new_position = current_position - amount;
            if new_position <= 0 {
                number_passed_zero = (-new_position) / 100;
            }

            (new_position % 100, number_passed_zero)
        },
        Direction::RIGHT => {
            let new_position = current_position + amount;
            if new_position >= 100 {
                number_passed_zero = new_position / 100;
            }

            (new_position % 100, number_passed_zero)
        },
    }
}

fn count_zeros(rotations: Vec<&str>) {
    let mut dial_position = 50;

    let mut pointed_at_zero = 0;

    let mut number_passed_zero;
    let mut passed_zero = 0;

    for rotation in rotations {
        (dial_position, number_passed_zero) = move_dial(dial_position, rotation);

        if dial_position == 0 {
            pointed_at_zero += 1;
        }

        passed_zero += number_passed_zero;
    }

    println!("Pointed at zero: {pointed_at_zero}");
    println!("Passed zero: {passed_zero}");
}
