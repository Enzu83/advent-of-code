use std::{collections::HashSet, fs::File, io::Read};

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

enum Operation {
    Nop,
    Acc,
    Jmp,
}

struct Instruction {
    operation: Operation,
    argument: i32,
}

fn decode_line(line: &str) -> Instruction {
    let (operation, argument) = line.split_once(" ").unwrap();

    // get argument value depending on the first char: '+' or '-'
    let mut argument = argument.chars();
    let value = match argument.next().unwrap() {
        '+' => argument.as_str().parse::<i32>().unwrap(),
        '-' => -argument.as_str().parse::<i32>().unwrap(),
        other => {
            println!("Unknown sign for argument: {other}");
            0
        },
    };

    match operation {
        "nop" => Instruction { operation: Operation::Nop, argument: value },
        "acc" => Instruction { operation: Operation::Acc, argument: value },
        "jmp" => Instruction { operation: Operation::Jmp, argument: value },
        other => {
            println!("Unknown operation: {other}");
            Instruction { operation: Operation::Nop, argument: 0 }
        },
    }
}

fn execute(instruction: &Instruction, accumulator: &mut i32) -> i32 {
    match instruction.operation {
        Operation::Nop => 1,
        Operation::Acc => {
            *accumulator += instruction.argument;
            1
        },
        Operation::Jmp => instruction.argument,
    }
}

fn puzzle_1(mut input: File) {
    let instructions: Vec<Instruction> = read_input(&mut input)
        .lines()
        .map(|line| decode_line(line))
        .collect();

    // stored executed instructions to know when the loop happens
    let mut visited = HashSet::<i32>::new();

    let mut pointer = 0; // pointer to the next instruction to be executed
    let mut accumulator = 0;

    // execute instructions while we haven't found a loop yet
    while !visited.contains(&pointer) {
        visited.insert(pointer);
        pointer += execute(&instructions[pointer as usize], &mut accumulator);

    }

    println!("Value of accumulator before loop {accumulator}");
}

fn puzzle_2(mut input: File) {
    // do the same thing as the first part but by switch a jmp to nop
    // see if it terminates by looking at how many instructions has been visited
    println!("{}", read_input(&mut input));
}