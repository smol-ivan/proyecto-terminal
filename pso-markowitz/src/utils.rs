use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn obtener_datos_prueba(filepath: &String) {
    let file = File::open(filepath).expect("No se pudo abrir el archivo de prueba.");
    let reader = BufReader::new(file);

    let mut lineas = reader.lines().map(|l| l.unwrap());

    let n_activos: i32  = lineas.next().unwrap().parse().unwrap();
    println!("{:?}", n_activos);
    
}
