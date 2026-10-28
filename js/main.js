// Helper function to initialize svg-pan-zoom for a given set of IDs
function setupSvgPanZoom(svgId, zoomInId, zoomOutId, resetId) {
    const embedEl = document.getElementById(svgId);
    if (!embedEl) return;

    embedEl.addEventListener('load', function() {
        const panZoom = svgPanZoom('#' + svgId, {
            zoomEnabled: true,
            controlIconsEnabled: false,
            fit: true,
            center: true,
            minZoom: 0.5,
            maxZoom: 10
        });

        document.getElementById(zoomInId)?.addEventListener('click', function(e) {
            e.preventDefault();
            panZoom.zoomIn();
        });

        document.getElementById(zoomOutId)?.addEventListener('click', function(e) {
            e.preventDefault();
            panZoom.zoomOut();
        });

        document.getElementById(resetId)?.addEventListener('click', function(e) {
            e.preventDefault();
            panZoom.resetZoom();
            panZoom.center();
        });
    });
}

// Initialize both graphs
document.addEventListener('DOMContentLoaded', () => {
    setupSvgPanZoom('theoretical-svg', 'theoretical-zoom-in', 'theoretical-zoom-out', 'theoretical-zoom-reset');
    setupSvgPanZoom('conceptual-svg', 'conceptual-zoom-in', 'conceptual-zoom-out', 'conceptual-zoom-reset');
});

// Same thing for the PNG file (RDF Grapher)
document.addEventListener('DOMContentLoaded', () => {
    const element = document.getElementById('rdf-png');
    
    // Inizializza Panzoom sull'immagine PNG
    const panzoom = Panzoom(element, {
        maxScale: 10,
        minScale: 0.5,
        contain: 'outside'
    });

    // Abilita lo zoom con la rotellina del mouse sopra l'immagine
    element.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

    // Gestione del click sui pulsanti
    document.getElementById('rdf-zoom-in')?.addEventListener('click', (e) => {
        e.preventDefault();
        panzoom.zoomIn();
    });

    document.getElementById('rdf-zoom-out')?.addEventListener('click', (e) => {
        e.preventDefault();
        panzoom.zoomOut();
    });

    document.getElementById('rdf-zoom-reset')?.addEventListener('click', (e) => {
        e.preventDefault();
        panzoom.reset();
    });
});