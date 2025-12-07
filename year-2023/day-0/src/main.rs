use std::fs::File;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let _ = File::open(",/input.txt")?;

    Ok(())
}
