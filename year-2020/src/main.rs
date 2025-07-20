use std::env::{args, current_dir};
use std::path::PathBuf;
use std::fs::File;

fn main() {
    // retrieve day number
    let args: Vec<String> = args().collect();
    let day = args[1].parse::<u8>().unwrap();
    let puzzle = args[2].parse::<u8>().unwrap();

    // open correspding input file
    let mut project_path = current_dir().unwrap();
    let input_path: PathBuf = ["inputs", format!("day{}", day).as_str(), "input.txt"].iter().collect();
    project_path.push(input_path);
    let input = File::open(project_path.as_os_str()).unwrap();

    // run the solution
    let runners: Vec<fn(u8, File)> = vec![
        year_2020::day0::run_puzzle,
        year_2020::day1::run_puzzle,
        year_2020::day2::run_puzzle,
        year_2020::day3::run_puzzle,
        year_2020::day4::run_puzzle,
        year_2020::day5::run_puzzle,
        year_2020::day6::run_puzzle,
    ];

    if let Some(run) = runners.get(day as usize) {
        run(puzzle, input);
    } else {
        panic!("Got an unexisting day number");
    }
}