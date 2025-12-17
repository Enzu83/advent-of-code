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

    let jboxes: Vec<JBox> = input
        .trim()
        .split("\n")
        .map(|s| JBox::from_str(s))
        .collect();

    let mut map = Map::new(jboxes);
    map.compute_distances();
    
    
    for _ in 0..1000 {
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
        let mut hashmap_distances = HashMap::new();
        for jbox_1 in self.jboxes.iter() {
            for jbox_2 in self.jboxes.iter() {
                if jbox_1 == jbox_2 {
                    continue;
                }

                let dist = jbox_1.distance(jbox_2);

                if !hashmap_distances.contains_key(&(jbox_1.clone(), jbox_2.clone())) && !hashmap_distances.contains_key(&(jbox_2.clone(), jbox_1.clone())) {
                    hashmap_distances.insert((jbox_1.clone(), jbox_2.clone()), dist);
                }
                
            }
        }

        self.distances = hashmap_distances.into_iter().collect();

        // sort by distances in descending order
        self.distances.sort_by(|(_, dist_1), (_, dist_2)| dist_1.partial_cmp(dist_2).unwrap());
        self.distances.reverse();
    }

    pub fn make_connection(&mut self) {
        if self.distances.len() == 0 {
            return;
        }

        let (jbox_1, jbox_2) = self.find_closest_not_connected_jboxes();

        // don't connect the jboxes if they already belong to a circuit
        if self.circuits.iter().any(|s| s.contains(&jbox_1) && s.contains(&jbox_2)) {
            return;
        }

        self.connections.insert((jbox_1.clone(), jbox_2.clone()));
        self.connections.insert((jbox_2.clone(), jbox_1.clone()));

        match (self.get_jbox_circuit(&jbox_1), self.get_jbox_circuit(&jbox_2)) {
            (Some(idx_1), Some(idx_2)) => {
                let c_2 = self.circuits[idx_2].clone();
                self.circuits[idx_1].extend(c_2);
                self.circuits.remove(idx_2);
            },
            (Some(idx_1), None) => {
                self.circuits[idx_1].insert(jbox_2);
            },
            (None, Some(idx_2)) => {
                self.circuits[idx_2].insert(jbox_1);
            },
            (None, None) => {
                let c = HashSet::from([jbox_1, jbox_2]);
                self.circuits.push(c);
            },
        }
    }

    fn find_closest_not_connected_jboxes(&mut self) -> (JBox, JBox) {
        let (mut jboxes, _) = self.distances.pop().unwrap();

        while self.connections.contains(&jboxes) {
            (jboxes, _) = self.distances.pop().unwrap();
        }

        jboxes
    }

    fn get_jbox_circuit(&self, jbox: &JBox) -> Option<usize> {
        for (idx, circuit) in self.circuits.iter().enumerate() {
            if circuit.contains(jbox) {
                return Some(idx)
            }
        }

        None
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
        
        
        for _ in 0..10 {
            map.make_connection();
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