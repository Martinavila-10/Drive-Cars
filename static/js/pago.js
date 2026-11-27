const numeroTarjeta = document.getElementById('numero_tarjeta');

if (numeroTarjeta) {
    numeroTarjeta.addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, '').slice(0, 16);
    });
}

const vencimiento = document.getElementById('vencimiento');

if (vencimiento) {
    vencimiento.addEventListener('input', function () {
        let valor = this.value.replace(/\D/g, '').slice(0, 4);

        if (valor.length > 2) {
            valor = valor.slice(0, 2) + '/' + valor.slice(2);
        }

        this.value = valor;
    });
}

const cvv = document.getElementById('cvv');

if (cvv) {
    cvv.addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, '').slice(0, 3);
    });
}
