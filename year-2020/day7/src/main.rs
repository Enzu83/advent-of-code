use std::{collections::{HashMap, HashSet}, error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day7.txt")?;
    
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

fn from_content_to_bag_info(content: &str) -> (String, u32) {
    if content == "no other bags" {
       return (String::new(), 0)
    }
    
    if let Some((amount, bag)) = content.split_once(" ") {
        let amount: u32 = amount.parse().unwrap();
        
        let bag = match amount {
            1 => bag[0..bag.len()-4].to_string(),
            _ => bag[0..bag.len()-5].to_string(),
        };

        (bag, amount)
    } else {
        println!("Failed to parse the bag content.");
        (String::new(), 0)
    }
}

fn decode_rule_for_where_bags_are_contained(where_bags_are_contained: &mut HashMap<String, HashMap<String, u32>>, rule: &str) {
    // separate container bag and contained bags (after removing the last char '.')
    if let Some((bag , contents)) = rule[0..rule.len()-1].split_once(" contain ") {
        // bag string used for hash map key
        let bag = bag[0..bag.len()-5].to_string();

        // created vector of bags that are contained with their numbers
        let contents: Vec<(String, u32)> = contents.split(", ")
            .map(|s| from_content_to_bag_info(s))
            .collect();

        // construct the bag hash map
        // it indicates where bags are contained
        for (contained_bag, amount) in contents {
            if contained_bag != "" {
                where_bags_are_contained.entry(contained_bag)
                    .or_insert(HashMap::from([(bag.clone(), amount)]))
                    .insert(bag.clone(), amount);
            }
        }
    }
}

fn get_bags_containers_for_a_bag(where_bags_are_contained: &HashMap<String, HashMap<String, u32>>, desired_bag: &str) -> HashSet<String> {
    let mut bags_containing_desired_bag = HashSet::new();
    
    let mut remaining_bags = vec![desired_bag];

    while !remaining_bags.is_empty() {
        let current_bag = remaining_bags.pop().unwrap();

        match where_bags_are_contained.get(current_bag) {
        Some(bags) => {
            for new_bag in bags.keys() {
                if !bags_containing_desired_bag.contains(new_bag) {
                    bags_containing_desired_bag.insert(new_bag.clone());
                    remaining_bags.push(new_bag);
                }
            }
        },
        None => {},
    }
    }

    bags_containing_desired_bag
}

fn decode_rule_for_what_bags_contain(what_bags_contain: &mut HashMap<String, HashMap<String, u32>>, rule: &str) {
    // separate container bag and contained bags (after removing the last char '.')
    if let Some((bag , contents)) = rule[0..rule.len()-1].split_once(" contain ") {
        // bag string used for hash map key
        let bag = bag[0..bag.len()-5].to_string();

        // created vector of bags that are contained with their numbers
        let contents: Vec<(String, u32)> = contents.split(", ")
            .map(|s| from_content_to_bag_info(s))
            .collect();

        // construct the bag hash map
        let mut contents_hash_map: HashMap<String, u32> = HashMap::new();

        for (contained_bag, amount) in contents {
            if contained_bag != "" {
                contents_hash_map.insert(contained_bag, amount);
            } else {
                contents_hash_map.insert(contained_bag, amount);
            }
        }

        what_bags_contain.insert(bag, contents_hash_map);
    }
}

fn get_how_many_bags_are_contained(what_bags_contain: &mut HashMap<String, HashMap<String, u32>>, desired_bag: &str) -> u32 {
    let mut number_of_bags = 0;

    let mut remaining_bags: Vec<(String, u32)> = what_bags_contain.get(desired_bag).unwrap()
        .iter().map(|(k, v)| (k.clone(), *v))
        .collect();

    while !remaining_bags.is_empty() {
        let (current_bag, amount) = remaining_bags.pop().unwrap();

        number_of_bags += amount;

        for (contained_bag, contained_bag_amount) in what_bags_contain.get(&current_bag).unwrap() {
            if contained_bag != "" {
                remaining_bags.push((contained_bag.clone(), *contained_bag_amount * amount));
            }
        }
    }

    number_of_bags
}

fn part_1(input: &String) {
    // indicate which bags (values) contain the bag (key)
    let mut where_bags_are_contained = HashMap::new();

    input
        .lines()
        .for_each(|rule| decode_rule_for_where_bags_are_contained(&mut where_bags_are_contained, rule));

    let desired_bag = "shiny gold";

    println!("Number of bags containing '{}': {}", desired_bag, get_bags_containers_for_a_bag(&where_bags_are_contained, desired_bag).len());
}

fn part_2(input: &String) {
    // indicate which bags (values) contain the bag (key)
    let mut what_bags_contain = HashMap::new();

    input
        .lines()
        .for_each(|rule| decode_rule_for_what_bags_contain(&mut what_bags_contain, rule));

    let desired_bag = "shiny gold";

    println!("Number of bags in '{}': {}", desired_bag, get_how_many_bags_are_contained(&mut what_bags_contain, desired_bag));
}
