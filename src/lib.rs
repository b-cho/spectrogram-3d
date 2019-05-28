#[macro_use]
extern crate stdweb;

use num::Complex;

use stdweb::js_export;
use stdweb::Array;
use stdweb::web::TypedArray;

fn dft(signal: Vec<i16>) -> Vec<Complex<f64>> {
    use std::f64::consts::PI;

    let N = signal.len();
    let mut output: Vec<Complex<f64>> = vec![];

    for k in 0..N/2 {
        let sum = signal.iter().enumerate().map(|(n, x)| {
            // e^((-2πikn)/N) * x
            Complex::i().scale(
                (PI * -2.0 * (k as f64) * (n as f64)) / (N as f64)
            ).exp().scale(*x as f64)
        // Sums the frequency bin values.
        }).fold(Complex::new(0.0, 0.0), |partial_sum, value| partial_sum + value);

        // Add the sum of this frequency bin's Fourier transform to the result matrix.
        output.push(sum);
    }

    output
}

#[js_export]
fn stft(input: TypedArray<u8>) -> Array {
    use std::convert::TryInto;

    // The signal is passed as an array of bytes; we assume that we are
    // consuming PCM (pulse-code modulation) with a bit depth of 16.
    let signal = input.to_vec().windows(2).map(
        |bytes| i16::from_le_bytes(bytes.try_into().unwrap())
    ).collect::<Vec<i16>>();

    let window_size: isize = 128;
    let overlap = window_size / 2;

    let mut output: Vec<Vec<Complex<f64>>> = vec![];

    for n in (0..signal.len()).step_by(window_size as usize) {
        let start = (n as isize - overlap).max(0) as usize;
        let end = (start as isize + window_size).min(signal.len() as isize) as usize;
        let window = &signal[start..end];
        
        let sums = dft(Vec::from(window));
        output.push(sums);
    }

    Array::from(output.iter().map(|window| {
        Array::from(window.iter().map(|bin_sum| {
            bin_sum.norm()
        }).collect::<Vec<_>>())
    }).collect::<Vec<_>>())
}
