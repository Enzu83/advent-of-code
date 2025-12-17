use std::collections::HashSet;
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

    let jboxes: Vec<JBox> = input
        .trim()
        .split("\n")
        .map(|s| JBox::from_str(s))
        .collect();

    let mut map = Map::new(jboxes);
    map.compute_distances();
    
    
    for _ in 0..1001 {
        map.make_connection();
    }

    map.circuits.sort_by_key(|s| s.len());
    map.circuits.reverse();

    let sizes: Vec<usize> = map.circuits
        .iter()
        .map(|s| s.len())
        .collect();

    println!("Three largest circuit sizes multiplied: {}", sizes[0] * sizes[1] * sizes[2]);

    Ok(())
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
struct JBox {
    x: i32,
    y: i32,
    z: i32,
}

impl JBox {
    pub fn new(x: i32, y: i32, z: i32) -> Self {
        Self { x, y, z }
    }

    pub fn from_str(string: &str) -> Self {
        let mut splitted_str = string.split(",");
        let x = splitted_str.next().unwrap().parse().unwrap();
        let y = splitted_str.next().unwrap().parse().unwrap();
        let z = splitted_str.next().unwrap().parse().unwrap();

        Self::new(x, y, z)
    }

    pub fn distance(&self, other: &JBox) -> f32 {
        let dx = (self.x - other.x) as f32;
        let dy = (self.y - other.y) as f32;
        let dz = (self.z - other.z) as f32;

        (dx*dx + dy*dy + dz*dz).sqrt()
    }
}

struct Map {
    jboxes: Vec<JBox>,
    distances: Vec<((JBox, JBox), f32)>,
    circuits: Vec<HashSet<JBox>>,
    connections: HashSet<(JBox, JBox)>,
}

impl Map {
    pub fn new(jboxes: Vec<JBox>) -> Self {
        Self {
            jboxes,
            distances: Vec::new(),
            circuits: Vec::new(),
            connections: HashSet::new(),
        }
    }

    pub fn compute_distances(&mut self) {
        for jbox_1 in self.jboxes.iter() {
            for jbox_2 in self.jboxes.iter() {
                if jbox_1 == jbox_2 {
                    continue;
                }

                let dist = jbox_1.distance(jbox_2);
                self.distances.push(((jbox_1.clone(), jbox_2.clone()), dist));
            }
        }

        // sort by distances in descending order
        self.distances.sort_by(|(_, dist_1), (_, dist_2)| dist_1.partial_cmp(dist_2).unwrap());
        self.distances.reverse();
    }

    pub fn make_connection(&mut self) {
        if self.distances.len() == 0 {
            return;
        }

        let (jbox_1, jbox_2) = self.find_closest_not_connected_jboxes();
        
        self.connections.insert((jbox_1.clone(), jbox_2.clone()));
        self.connections.insert((jbox_2.clone(), jbox_1.clone()));

        for (_, circuit) in self.circuits.iter_mut().enumerate() {            
            if circuit.contains(&jbox_1) || circuit.contains(&jbox_2) {
                circuit.insert(jbox_1.clone());
                circuit.insert(jbox_2.clone());
                return;
            }
        }

        let new_circuit = HashSet::from([jbox_1.clone(), jbox_2.clone()]);
        self.circuits.push(new_circuit);
    }

    fn find_closest_not_connected_jboxes(&mut self) -> (JBox, JBox) {
        let (mut jboxes, _) = self.distances.pop().unwrap();

        while self.connections.contains(&jboxes) {
            (jboxes, _) = self.distances.pop().unwrap();
        }

        jboxes
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn example() {
        let input = "162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689";

        let jboxes: Vec<JBox> = input
            .trim()
            .split("\n")
            .map(|s| JBox::from_str(s))
            .collect();

        let mut map = Map::new(jboxes);
        map.compute_distances();
        
        
        for _ in 0..11 {
            map.make_connection();
        }

        println!("{:?}", &map.distances[0..30]);
        println!();

        for c in map.circuits.iter() {
            println!("{:?}", c);
        }

        map.circuits.sort_by_key(|s| s.len());
        map.circuits.reverse();

        let sizes: Vec<usize> = map.circuits
            .iter()
            .map(|s| s.len())
            .collect();

        assert_eq!(sizes[0] * sizes[1] * sizes[2], 40);
    }
}