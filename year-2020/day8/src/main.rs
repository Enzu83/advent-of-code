use std::{collections::HashSet, error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day8.txt")?;
    
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

#[derive(Debug, Clone)]
enum Operation {
    Nop,
    Acc,
    Jmp,
}

#[derive(Debug, Clone)]
struct Instruction {
    operation: Operation,
    argument: i32,
}

impl Instruction {
    pub fn replace_operation(&mut self, new_operation: Operation) {
        self.operation = new_operation;
    }
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

fn execute(instruction: &Instruction, accumulator: &mut i32) -> usize {
    match instruction.operation {
        Operation::Nop => 1,
        Operation::Acc => {
            *accumulator += instruction.argument;
            1
        },
        Operation::Jmp => instruction.argument as usize,
    }
}

fn execute_until_loop(instructions: &Vec<Instruction>) -> (i32, bool) {
    // stored executed instructions to know when the loop happens
    let mut visited = HashSet::<usize>::new();

    let mut pointer = 0; // pointer to the next instruction to be executed
    let mut accumulator = 0;

    // execute instructions while we haven't found a loop yet
    while pointer < instructions.len() && !visited.contains(&pointer) {
        visited.insert(pointer);
        pointer += execute(&instructions[pointer], &mut accumulator);
    }

    (accumulator, pointer == instructions.len())
}

fn part_1(input: &String) {
    let instructions: Vec<Instruction> = input
        .lines()
        .map(|line| decode_line(line))
        .collect();

    let (accumulator, _) = execute_until_loop(&instructions);

    println!("Value of accumulator before loop: {accumulator}");
}

fn part_2(input: &String) {
    // do the same thing as the first part but by switch a jmp to nop
    // see if it terminates by looking at how many instructions has been visited

    let instructions: Vec<Instruction> = input
        .lines()
        .map(|line| decode_line(line))
        .collect();

    for i in 0..instructions.len() {
        let mut new_instructions = instructions.clone();

        match new_instructions[i].operation {
            Operation::Jmp => new_instructions[i].replace_operation(Operation::Nop),
            Operation::Nop => new_instructions[i].replace_operation(Operation::Jmp),
            Operation::Acc => continue,
        };

        let (accumulator, terminate) = execute_until_loop(&new_instructions);

        if terminate {
            println!("Value of accumulator when the program terminates: {accumulator}");
            break;
        }
    };
}
