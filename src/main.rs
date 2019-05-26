use stdweb::traits::*;
use stdweb::unstable::TryInto;

use stdweb::web::{
    document,
    window,
    CanvasRenderingContext2d
};

use stdweb::web::html_element::CanvasElement;

fn main() {
    stdweb::initialize();

    let canvas: CanvasElement = document().query_selector("#canvas")
        .unwrap().unwrap().try_into().unwrap();
    
    let context: CanvasRenderingContext2d = canvas.get_context().unwrap();

    canvas.set_width(500);
    canvas.set_height(500);

    stdweb::event_loop();
}
