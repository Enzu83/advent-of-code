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

    let worksheet = Worksheet::from_sheet(&input);
    println!("Sum of answers: {}", worksheet.solve());

    let worksheet = Worksheet::from_sheet_right_to_left(&input);
    println!("Sum of answers (right to left): {}", worksheet.solve());

    Ok(())
}

#[derive(Clone, Debug)]
enum Operation {
    ADD,
    MUL,
}

impl Operation {
    pub fn parse(s: &str) -> Result<Self, Box<dyn Error>> {
        match s {
            "+" => Ok(Operation::ADD),
            "*" => Ok(Operation::MUL),
            other => Err(format!("unknown operation: {other}").into()),
        }
    }
}

#[derive(Debug)]
struct Problem {
    numbers: Vec<i64>,
    operation: Operation,
}

impl Problem {
    pub fn new(numbers: Vec<i64>, operation: Operation) -> Self {
        Self { numbers, operation }
    }

    pub fn solve(&self) -> i64 {
        let mut res = self.numbers[0];

        for val in self.numbers[1..].iter() {
            res = self.compute_operation(res, *val);
        }

        res
    }

    fn compute_operation(&self, a: i64, b: i64) -> i64 {
        match self.operation {
            Operation::ADD => a + b,
            Operation::MUL => a * b,
        }
    }
}

enum Row {
    NUMBER(Vec<i64>),
    OPERATION(Vec<Operation>),
}

struct Worksheet {
    problems: Vec<Problem>,
}

impl Worksheet {
    pub fn new() -> Self {
        Self { problems: Vec::new() }
    }

    pub fn from_sheet(sheet: &str) -> Self {
        let mut numbers: Vec<Vec<i64>> = Vec::new();
        let mut operations: Vec<Operation> = Vec::new();

        for row in sheet.trim().split("\n") {
            match Worksheet::parse_row(row) {
                Row::NUMBER(row_numbers) => numbers.push(row_numbers),
                Row::OPERATION(row_operations) => operations = row_operations,
            }
        }

        let mut worksheet = Self::new();

        for (i, op) in operations.iter().enumerate() {
            let mut val = Vec::new();
            numbers.iter().for_each(|v| val.push(v[i]));

            let problem = Problem::new(val, op.clone());
            worksheet.problems.push(problem);
        }

        worksheet
    }

    fn parse_row(row: &str) -> Row {
        let elements: Vec<&str> = row.split_whitespace().collect();

        match elements[0].parse::<i64>() {
            Ok(_) => {
                Row::NUMBER(
                    elements.iter().map(|s| s.parse::<i64>().unwrap()).collect()
                )
            },
            Err(_) => {
                Row::OPERATION(
                    elements.iter().map(|s| Operation::parse(s).unwrap()).collect()
                )
            }
        }
    }

    pub fn from_sheet_right_to_left(sheet: &str) -> Self {
        let mut rows: Vec<&str> = sheet.split("\n").collect();
        if rows[rows.len()-1] == "" {
            rows.pop();
        }

        let mut numbers: Vec<Vec<i64>> = Vec::new();
        let mut operations = Vec::new();
        
        for i in 0..rows[0].len() {
            if let Ok(op) = Operation::parse(&rows[rows.len()-1][i..i+1]) {
                operations.push(op);
                numbers.push(Vec::new());
            }

            let num: String = (0..rows.len()-1)
                .map(|j| rows[j][i..i+1].chars().next().unwrap())
                .collect::<String>()
                .trim()
                .to_string();

            if let Ok(num) = num.parse::<i64>() {
                let idx = numbers.len()-1;
                numbers[idx].push(num);
            }
        }

        let mut worksheet = Self::new();
        for (i, op) in operations.iter().enumerate() {
            let problem = Problem::new(
                numbers[i].clone(),
                op.clone()
            );

            worksheet.problems.push(problem);
        }

        worksheet
    }

    pub fn solve(&self) -> i64 {
        self.problems.iter()
            .map(|p| p.solve())
            .sum()
        }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn example() {
        let input = "123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  ";

        let worksheet = Worksheet::from_sheet(input);
        assert_eq!(worksheet.solve(), 4277556);

        let worksheet = Worksheet::from_sheet_right_to_left(input);
        assert_eq!(worksheet.solve(), 3263827);
    }

    #[test]
    fn solve_problem() {
        let p = Problem::new(
            vec![123, 45, 6],
            Operation::MUL,
        );
        assert_eq!(p.solve(), 33210);

        let p = Problem::new(
            vec![328, 64, 98],
            Operation::ADD,
        );
        assert_eq!(p.solve(), 490);

        let p = Problem::new(
            vec![51, 387, 215],
            Operation::MUL,
        );
        assert_eq!(p.solve(), 4243455);

        let p = Problem::new(
            vec![64, 23, 314],
            Operation::ADD,
        );
        assert_eq!(p.solve(), 401);
    }
}