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

        // Fase 1: renderiza marcadores e lista
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

        // Fase 2: busca lenta de detalhes (se quiser enriquecer)
        enriquecerPopupsComDetalhes();

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

// Função para enriquecer popups com detalhes extras do cache
function enriquecerPopupsComDetalhes() {
  markers.forEach(({ marker, ponto }, i) => {
    if (!ponto.place_id) return;

    setTimeout(() => {
      $.get(`/detalhes`, { place_id: ponto.place_id })
        .done(function (detalhes) {
          let popupContent = `<strong>${detalhes.nome}</strong><br>${detalhes.tipo}`;
          if (detalhes.endereco) {
            popupContent += `<br>${detalhes.endereco}`;
          }
          popupContent += `
            <br><a href="https://www.google.com/maps/dir/?api=1&destination=${detalhes.lat},${detalhes.lon}" target="_blank">🗺️ Ir com Google Maps</a>
            <br><a href="https://waze.com/ul?ll=${detalhes.lat},${detalhes.lon}&navigate=yes" target="_blank">🚗 Ir com Waze</a>
          `;
          marker.bindPopup(popupContent);
        })
        .fail(function (err) {
          console.warn(`Não foi possível buscar detalhes de ${ponto.nome}`);
        });
    }, i * 300); // espaçamento para evitar sobrecarga
  });
}
