use std::{error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day9.txt")?;
    
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

fn find_first_non_valid(numbers: &[u32]) {

}

fn is_next_valid(sums: &Vec<[u32; 25]>) -> bool {
    false
}

fn part_1(input: &String) {
    let numbers: Vec<u32> = input
        .lines()
        .map(|s| s.parse().unwrap())
        .collect();
}

fn part_2(input: &String) {
    println!("{}", input);
}
