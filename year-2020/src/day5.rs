use std::{fs::File, io::Read};

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

fn get_seats(input: &mut File) -> Vec<Seat> {
    read_input(input)
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


fn puzzle_1(mut input: File) {
    let seats = get_seats(&mut input);

    let highest_id = seats.iter().map(|seat| seat.id()).max().unwrap();

    println!("Highest ID: {}", highest_id);
}

fn puzzle_2(mut input: File) {
    let seats = get_seats(&mut input);

    // the empty seat can be seen in the print
    print_seats(&seats);
}