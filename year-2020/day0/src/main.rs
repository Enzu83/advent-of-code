use std::{error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day0.txt")?;
    
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

fn part_1(input: &String) {
    println!("{input}");
}

fn part_2(input: &String) {
    println!("{input}");
}