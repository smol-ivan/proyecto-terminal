mod utils;

use crate::utils::*;
use std::env;

fn main() {
    println!("Hello, world!");
    let args: Vec<String> = env::args().collect();

    if args.len() < 4 {
        eprintln!("Uso: ${} <filepath to test>", args[0]);
        return;
    }

    let filepath = &args[1];
}
