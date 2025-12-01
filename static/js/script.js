$(document).ready(function () {
  let map;
  let markers = [];

  $('#buscar').click(function () {
    const endereco = $('#endereco').val();
    $('#buscar').text('Buscando...').prop('disabled', true);

    $.get('/pontos', { endereco }, function (data) {
      $('#resultados').empty();
      markers = [];

      if (map) {
        map.remove();
      }

      if (data.length > 0) {
        const lat = data[0].lat;
        const lon = data[0].lon;

        map = L.map('map').setView([lat, lon], 14);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        data.forEach((ponto, index) => {
          const popupContent = `
            <strong>${ponto.nome}</strong><br>
            ${ponto.tipo}<br>
            ${ponto.endereco ? ponto.endereco + '<br>' : ''}
            <br><a href="https://www.google.com/maps/dir/?api=1&destination=${ponto.lat},${ponto.lon}" target="_blank">🗺️ Google Maps</a>
            <br><a href="https://waze.com/ul?ll=${ponto.lat},${ponto.lon}&navigate=yes" target="_blank">🚗 Waze</a>
          `;

          const marker = L.marker([ponto.lat, ponto.lon])
            .addTo(map)
            .bindPopup(popupContent);

          markers.push({ marker, ponto });

          $('#resultados').append(`
            <li>
              <a href="#" class="focar" data-index="${index}">${ponto.nome}</a> - ${ponto.tipo}
            </li>
          `);
        });

      } else {
        $('#resultados').append('<li>Nenhum ponto turístico encontrado.</li>');
      }

      $('#buscar').text('Buscar').prop('disabled', false);
    });
  });

  $('#resultados').on('click', '.focar', function (e) {
    e.preventDefault();
    $('#resultados li').removeClass('ativo');
    $(this).parent().addClass('ativo');

    const index = $(this).data('index');
    const item = markers[index];
    if (item && item.marker) {
      map.setView(item.marker.getLatLng(), 16, { animate: true });
      item.marker.openPopup();
      document.getElementById('map').scrollIntoView({ behavior: 'smooth' });
    }
  });
});
