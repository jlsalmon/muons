//var fromProjection = new ol.Projection("EPSG:4326");   // Transform from WGS 1984
//var toProjection = new ol.Projection("EPSG:900913"); // to Spherical Mercator Projection
//var position = new ol.LonLat(13.41, 52.52);//.transform(fromProjection, toProjection);

var delay = 0;
var map;
var map_data;
var map_data2;

function show_map() {
    var raster = new ol.layer.Tile({
        source: new ol.source.Stamen({
            layer: 'toner',
            opacity: 0.2
        })
    });

    map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.MapQuest({layer: 'osm'}),
                opacity: 0.8
            }),

            raster
        ],
        target: 'map',
        view: new ol.View({
            center: ol.proj.transform([6.055279, 46.232991],
                'EPSG:4326', 'EPSG:3857'),
            zoom: 15
        })
    });

    var pos = ol.proj.transform([6.055279, 46.232991], 'EPSG:4326', 'EPSG:3857');

    var featurecollection = {
        "type": "FeatureCollection",
        "features": [
            {"geometry": {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "LineString",
                        "coordinates": [
                            [11.0878902207, 45.1602390564],
                            [15.01953125, 48.1298828125]
                        ]
                    },
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [11.0878902207, 45.1602390564],
                                [14.931640625, 40.9228515625],
                                [0.8251953125, 41.0986328125],
                                [7.63671875, 48.96484375],
                                [11.0878902207, 45.1602390564]
                            ]
                        ]
                    },
                    {
                        "type": "Point",
                        "coordinates": [15.87646484375, 44.1748046875]
                    }
                ]
            },
                "type": "Feature",
                "properties": {}}
        ]
    };

    var feature = new ol.Feature({
        geometry: new ol.geom.Point([6.056279, 46.235991]),
        name: 'My Polygon'
    });

    feature.setStyle(new ol.style.Circle({
        radius: 50,
        fill: new ol.style.Fill({
            color: 'rgba(255, 153, 0, 0.4)'
        }),
        stroke: new ol.style.Stroke({
            color: 'rgba(255, 204, 0, 0.2)',
            width: 1
        })
    }));

    map.addLayer(new ol.layer.Vector({
        source: new ol.source.Vector({
            features: feature
        })
    }));
    map.render();
}


function animate_map(data, data2) {
    map_data = data;
    map_data2 = data2;

    map.once('postcompose', on_postcompose);

    map.render();
}

var i = 0;

function on_postcompose(event) {
    console.log('on postcompose');
    var vectorContext = event.vectorContext;
    var coordinates = [];

    coordinates.push(ol.proj.transform([6.055279, 46.232991],
        'EPSG:4326', 'EPSG:3857'));

    coordinates.push(ol.proj.transform([6.055513, 46.234222],
        'EPSG:4326', 'EPSG:3857'));

    delay = map_data[i][0];
    delay2 = map_data2[i][0];
    var radius = map_data[i][1];
    var radius2 = map_data2[i][1];
    i++;

    var style = new ol.style.Circle({
        radius: radius,
        fill: new ol.style.Fill({
            color: 'rgba(255, 153, 0, 0.4)'
        }),
        stroke: new ol.style.Stroke({
            color: 'rgba(255, 204, 0, 0.2)',
            width: 1
        })
    });

    var style2 = new ol.style.Circle({
        radius: radius2,
        fill: new ol.style.Fill({
            color: 'rgba(255, 153, 0, 0.4)'
        }),
        stroke: new ol.style.Stroke({
            color: 'rgba(255, 204, 0, 0.2)',
            width: 1
        })
    });

    vectorContext.setImageStyle(style);
    vectorContext.drawMultiPointGeometry(
        new ol.geom.MultiPoint(coordinates), null);

    vectorContext.setImageStyle(style2);
    vectorContext.drawMultiPointGeometry(
        new ol.geom.MultiPoint(coordinates), null);


    setTimeout(function () {
        map.once('postcompose', on_postcompose);
        map.render();
    }, delay)
}
