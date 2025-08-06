const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');

let mediaRecorder;
let audioChunks = [];

startBtn.addEventListener('click', async () => {
    // Ask for mic permission
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Create MediaRecorder instance
    mediaRecorder = new MediaRecorder(stream);

    // On data available, push audio chunks
    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    // On stop, create blob and play audio
    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;
        audioPlayback.play();
        audioChunks = []; // clear for next recording
    };

    // Start recording
    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
});

stopBtn.addEventListener('click', () => {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
});