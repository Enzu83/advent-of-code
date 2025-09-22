use std::{error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day5.txt")?;
    
    // solve both parts
    part_1(&input);
    part_2(&input);

    Ok(())
}

fn read_input(file_path: &str) -> Result<String, Box<dyn Error>> {
    let mut input = File::open(file_path)?;
    
    let mut content = String::new();
    input.read_to_string(&mut content)?;
    Ok(content)
}

struct Seat {
    row: usize,
    col: usize,
}

impl Seat {
    pub fn from(row: usize, col: usize) -> Self {
        Seat { row, col }
    }

    pub fn id(&self) -> usize {
        self.row * 8 + self.col
    }
}

fn decode_partition(partition: &str, lower_letter: &str, upper_letter: &str) -> usize {
    let mut binary_string = String::from(partition);
    binary_string = binary_string.replace(lower_letter, "0");
    binary_string = binary_string.replace(upper_letter, "1");

    usize::from_str_radix(&binary_string, 2).unwrap()
}

fn decode_seat(seat_partition: &str) -> Seat {
    let row = decode_partition(&seat_partition[0..7], "F", "B");
    let col = decode_partition(&seat_partition[7..], "L", "R");

    Seat::from(row, col)
}

fn get_seats(input: &String) -> Vec<Seat> {
    input
        .lines()
        .map(|seat_partition| decode_seat(seat_partition))
        .collect()
}

fn print_seats(seats: &Vec<Seat>) {
    let mut seat_print = vec![vec!['.'; 128]; 8];

    for seat in seats {
        seat_print[seat.col][seat.row] = '#';
    }

    for row in seat_print.iter() {
        println!("{}", row.iter().collect::<String>());
    }
}

fn part_1(input: &String) {
    let seats = get_seats(input);

    let highest_id = seats.iter().map(|seat| seat.id()).max().unwrap();

    println!("Highest ID: {}", highest_id);
}

fn part_2(input: &String) {
    let seats = get_seats(input);

    // the empty seat can be seen in the print
    print_seats(&seats);
}
