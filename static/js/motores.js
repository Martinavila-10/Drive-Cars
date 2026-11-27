document.querySelectorAll('.motor-player').forEach(player => {

    const audio = player.querySelector('.audio-motor');
    const boton = player.querySelector('.motor-play');
    const progreso = player.querySelector('.motor-progreso');
    const volumen = player.querySelector('.motor-control-volumen');
    const tiempoActual = player.querySelector('.motor-actual');
    const duracion = player.querySelector('.motor-duracion');
    const estado = player.querySelector('.motor-estado');

    audio.volume = Number(volumen.value);

    function formatoTiempo(segundos) {
        if (!Number.isFinite(segundos)) return '0:00';

        const minutos = Math.floor(segundos / 60);
        const segundosRestantes = Math.floor(segundos % 60);

        return `${minutos}:${String(segundosRestantes).padStart(2, '0')}`;
    }

    boton.addEventListener('click', () => {

        document.querySelectorAll('.motor-player').forEach(otroPlayer => {

            if (otroPlayer !== player) {
                const otroAudio = otroPlayer.querySelector('.audio-motor');

                otroAudio.pause();

                otroPlayer.querySelector('.motor-play').textContent = '▶';
                otroPlayer.querySelector('.motor-estado').textContent = 'READY';
            }

        });

        if (audio.paused) {

            audio.play().then(() => {
                boton.textContent = 'Ⅱ';
                estado.textContent = 'PLAYING';
            }).catch(() => {
                estado.textContent = 'ERROR';
            });

        } else {

            audio.pause();
            boton.textContent = '▶';
            estado.textContent = 'PAUSED';

        }

    });

    audio.addEventListener('loadedmetadata', () => {
        duracion.textContent = formatoTiempo(audio.duration);
    });

    audio.addEventListener('timeupdate', () => {

        tiempoActual.textContent = formatoTiempo(audio.currentTime);

        if (Number.isFinite(audio.duration) && audio.duration > 0) {
            progreso.value = (audio.currentTime / audio.duration) * 100;
        }

    });

    progreso.addEventListener('input', () => {

        if (Number.isFinite(audio.duration) && audio.duration > 0) {
            audio.currentTime = (progreso.value / 100) * audio.duration;
        }

    });

    volumen.addEventListener('input', () => {
        audio.volume = Number(volumen.value);
    });

    audio.addEventListener('ended', () => {

        boton.textContent = '▶';
        estado.textContent = 'FINISHED';

        progreso.value = 0;
        tiempoActual.textContent = '0:00';

    });

    audio.addEventListener('pause', () => {

        if (!audio.ended) {
            boton.textContent = '▶';
        }

    });

    audio.addEventListener('play', () => {
        boton.textContent = 'Ⅱ';
        estado.textContent = 'PLAYING';
    });

});
