import * as _ from "./opusrec/recorder.min.js";

export async function record() {
    const spectrogram = await Rust["spectrogram_3d"];

    console.log("Recording is supported? " + !!window.Recorder.isRecordingSupported());

    const recorder = new window.Recorder({
        encoderPath: "opusrec/waveWorker.min.js",
    });

    let n = 500;
    recorder.onrawdata = (data) => {
        if (n-- <= 0) return;

        const frequencies = spectrogram.stft(data);
        
        // TODO: Render to canvas.
        console.log(frequencies.length);
        console.log(frequencies);
    };

    recorder.start();
}
