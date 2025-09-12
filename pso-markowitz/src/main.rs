mod models;
mod utils;

use crate::models::*;
use crate::utils::*;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Uso: ${} <filepath to test>", args[0]);
        return;
    }

    obtener_datos_prueba(&args[1]);
}
