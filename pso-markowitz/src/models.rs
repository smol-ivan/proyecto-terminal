pub type Activos = Vec<Activo>;

pub struct Activo {
    pub id: usize,
    pub mean_return: f64,
    pub standard_deviation: f64,
}

pub struct Correlation {
    pub i: usize,
    pub j: usize,
    pub value: f64,
}
