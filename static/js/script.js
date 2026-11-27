const reproductor = document.getElementById("reproductor");
const disco = document.getElementById("disco");
const portadaCancion = document.getElementById("portadaCancion");
const estadoMusica = document.getElementById("estadoMusica");
const nombreCancion = document.getElementById("nombreCancion");
const nombreArtista = document.getElementById("nombreArtista");
const anterior = document.getElementById("anterior");
const siguiente = document.getElementById("siguiente");
const playPause = document.getElementById("playPause");
const contenedorDisco = disco.parentElement;

const playlist = [
    {
        archivo: "/static/musica/cancion1.mp3",
        nombre: "Desvelado",
        artista: "kessoku band",
        portada: "/static/img/portada1.jpg"
    },
    {
        archivo: "/static/musica/cancion2.mp3",
        nombre: "Tres Camionetas",
        artista: "Beto Quintanilla",
        portada: "/static/img/portada2.jpg"
    },
    {
        archivo: "/static/musica/cancion3.mp3",
        nombre: "cuatro camionetas",
        artista: "Beto Quitanilla",
        portada: "/static/img/portada3.jpg"
    },
    {
        archivo: "/static/musica/cancion4.mp3",
        nombre: "Pepe Guerra",
        artista: "Beto Quitanilla",
        portada: "/static/img/portada4.jpg"
    },
    {
        archivo: "/static/musica/cancion5.mp3",
        nombre: "Le Dije Al Corazon",
        artista: "Duelo",
        portada: "/static/img/portada5.jpg"
    },
    {
        archivo: "/static/musica/cancion6.mp3",
        nombre: "El Gordo Paz",
        artista: "Beto Quintanilla",
        portada: "/static/img/portada6.jpg"
    },
    {
        archivo: "/static/musica/cancion7.mp3",
        nombre: "La Mejor De Mis Tragedias",
        artista: "Los Invasores De Nuevo Leon",
        portada: "/static/img/portada,7.jpg"
    },
    {
        archivo: "/static/musica/cancion8.mp3",
        nombre: "Con Tu Imagen",
        artista: "Los Invasores De Nuevo Leon",
        portada: "/static/img/portada8.jpg"
    },
    {
        archivo: "/static/musica/cancion9.mp3",
        nombre: "Chico Enamorado",
        artista: "El Ezequiel",
        portada: "/static/img/portada9.jpg"
    },
    {
        archivo: "/static/musica/cancion10.mp3",
        nombre: "Someone To Spend Time With",
        artista: "Los Retros",
        portada: "/static/img/portada10.jpg"
    },
    {
        archivo: "/static/musica/cancion11.mp3",
        nombre: "El Centenario",
        artista: "Los Tucanes de Tijuana",
        portada: "/static/img/portada11.jpg"
    }
];

let cancionActual = 0;

function cargarCancion(indice, reproducir = false) {
    cancionActual = indice;
    const cancion = playlist[cancionActual];
    
    reproductor.pause();
    contenedorDisco.classList.remove("girando");
    
    reproductor.src = cancion.archivo;
    reproductor.load();
    
    nombreCancion.textContent = cancion.nombre;
    nombreArtista.textContent = cancion.artista;
    portadaCancion.src = cancion.portada;
    
    playPause.textContent = "▶";
    estadoMusica.textContent = "⏸ PAUSADO";
    
    if (reproducir) {
        reproducirCuandoEsteLista();
    }
}

function reproducirCuandoEsteLista() {
    if (reproductor.readyState >= 3) {
        reproducirCancion();
        return;
    }
    reproductor.addEventListener(
        "canplay",
        reproducirCancion,
        { once: true }
    );
}

function reproducirCancion() {
    reproductor.play()
        .then(function () {
            contenedorDisco.classList.add("girando");
            playPause.textContent = "⏸";
            estadoMusica.textContent = "▶ REPRODUCIENDO";
        })
        .catch(function (error) {
            console.log("Error de reproducción:", error);
        });
}

playPause.addEventListener("click", function () {
    if (reproductor.paused) {
        reproducirCancion();
    } else {
        reproductor.pause();
    }
});

reproductor.addEventListener("play", function () {
    contenedorDisco.classList.add("girando");
    playPause.textContent = "⏸";
    estadoMusica.textContent = "▶ REPRODUCIENDO";
});

reproductor.addEventListener("pause", function () {
    contenedorDisco.classList.remove("girando");
    playPause.textContent = "▶";
    estadoMusica.textContent = "⏸ PAUSADO";
});

siguiente.addEventListener("click", function () {
    cancionActual++;
    if (cancionActual >= playlist.length) {
        cancionActual = 0;
    }
    cargarCancion(cancionActual, true);
});

anterior.addEventListener("click", function () {
    cancionActual--;
    if (cancionActual < 0) {
        cancionActual = playlist.length - 1;
    }
    cargarCancion(cancionActual, true);
});

reproductor.addEventListener("ended", function () {
    cancionActual++;
    if (cancionActual >= playlist.length) {
        cancionActual = 0;
    }
    cargarCancion(cancionActual, true);
});

cargarCancion(0, false);