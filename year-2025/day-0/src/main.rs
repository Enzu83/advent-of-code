use std::env;
use std::fs::File;
use std::io::Read;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input_path = match env::args().nth(1) {
        Some(path) => path,
        None => panic!("Please specify a path for the input file."),
    };
    let mut file = File::open(input_path)?;
    let mut input = String::new();
    file.read_to_string(&mut input)?;

    println!("{input}");

    Ok(())
}
