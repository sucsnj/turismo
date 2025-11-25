let map;
let markers = [];

$(document).ready(function () {
  $('#buscar').click(function () {
    const endereco = $('#endereco').val();
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

        // Renderiza marcadores e lista
        data.forEach((ponto, index) => {
          const lat = ponto.lat;
          const lon = ponto.lon;

          const popupContent = `
            <strong>${ponto.nome}</strong><br>
            ${ponto.tipo}<br>
            ${ponto.endereco ? ponto.endereco + '<br>' : ''}
            <br><a href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}" target="_blank">🗺️ Ir com Google Maps</a>
            <br><a href="https://waze.com/ul?ll=${lat},${lon}&navigate=yes" target="_blank">🚗 Ir com Waze</a>
          `;

          const marker = L.marker([lat, lon])
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
    });
  });

  // Evento de clique nos links da lista
  $('#resultados').on('click', '.focar', function (e) {
    e.preventDefault();
    const index = $(this).data('index');
    const item = markers[index];
    if (item && item.marker) {
      map.setView(item.marker.getLatLng(), 16);
      item.marker.openPopup();
      document.getElementById('map').scrollIntoView({ behavior: 'smooth' });
    }
  });
});
