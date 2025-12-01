use std::fs::File;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open(",/input.txt")?;

    Ok(())
}
