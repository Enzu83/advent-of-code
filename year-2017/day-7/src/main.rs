use std::collections::{HashMap, HashSet};
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

    let programs = get_programs(&input);
    println!("Bottom program: {}", get_bottom_program(&programs));

    Ok(())
}

fn get_programs(input: &str) -> HashMap<String, HashSet<String>> {
    let mut programs = HashMap::new();

    for row in input.trim().split("\n") {
        match row.split_once("->") {
            None => {
                let name = row.split_whitespace().next().unwrap().to_string();
                programs.insert(name, HashSet::new());
            },
            Some((name_part, list_part)) => {
                let name = name_part
                    .split("(")
                    .next()
                    .unwrap()
                    .trim()
                    .to_string();
                
                let programs_list = list_part
                    .trim()
                    .split(",")
                    .map(|s| s.trim().to_string())
                    .collect();

                programs.insert(name, programs_list);
            },
        }
    }

    programs
}

fn get_bottom_program(programs: &HashMap<String, HashSet<String>>) -> &String {
    let all_programs: HashSet<&String> = programs.keys().collect();

    let mut not_bottom_programs = HashSet::new();
    for (_, disc_programs) in programs {
        not_bottom_programs.extend(disc_programs);
    }
 
    all_programs
        .difference(&not_bottom_programs)
        .into_iter()
        .next()
        .unwrap()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn programs() {
        let input = "pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)";

        let programs = get_programs(input);
        assert_eq!(get_bottom_program(&programs), "tknk");
    }
}