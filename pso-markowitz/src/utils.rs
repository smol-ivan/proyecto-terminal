use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn obtener_datos_prueba(filepath: &String) {
    let file = File::open(filepath).expect("No se pudo abrir el archivo de prueba.");
    let lines = BufReader::new(file).lines();
    println!("{:?}", lines);
}
