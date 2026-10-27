// node mkmap.js <name> <lat0> <lat1> <rotLon> <centerLat> <scale> <tx> <ty>  -> ../map_data_<name>.js
const topo = require('topojson-client'), d3 = require('d3-geo'), fs = require('fs');
const [name, p0, p1, rot, clat, scale, tx, ty] = process.argv.slice(2);
const w = JSON.parse(fs.readFileSync(require.resolve('world-atlas/countries-50m.json')));
const feats = topo.feature(w, w.objects.countries).features;
const REP = ['Russia','Ukraine','Belarus','Moldova','Estonia','Latvia','Lithuania','Georgia','Armenia','Azerbaijan','Kazakhstan','Uzbekistan','Turkmenistan','Kyrgyzstan','Tajikistan'];
const proj = d3.geoConicEqualArea().parallels([+p0, +p1]).rotate([-rot, 0]).center([0, +clat]).translate([+tx, +ty]).scale(+scale);
const path = d3.geoPath(proj);
const PTS = { Kabul:[69.17,34.53], Termez:[67.28,37.22], Kushka:[62.3,35.29], Moscow:[37.62,55.75], Berlin:[13.4,52.52], Chernobyl:[30.1,51.39],
  Vilnius:[25.28,54.69], Riga:[24.1,56.95], Tallinn:[24.75,59.44], Tbilisi:[44.8,41.72], Kyiv:[30.52,50.45], Minsk:[27.56,53.9], Baikonur:[63.3,45.9],
  Leningrad:[30.3,59.93], Baku:[49.87,40.41], Almaty:[76.9,43.25], Warsaw:[21.0,52.23], Prague:[14.42,50.08], Budapest:[19.04,47.5], Bucharest:[26.1,44.43],
  Sofia:[23.32,42.7], Foros:[33.78,44.39], Belovezha:[23.9,52.65], Stepanakert:[46.75,39.82], Brest:[23.66,52.1], Gdansk:[18.65,54.35], Kandahar:[65.7,31.6], Herat:[62.2,34.35], Tashkent:[69.24,41.3], Dushanbe:[68.78,38.56], Yerevan:[44.5,40.18], Chisinau:[28.86,47.01] };
const out = { rep: {}, named: {}, pts: {}, cent: {} };
function mainland(f){ if(f.geometry.type!=='MultiPolygon') return f; let best=null,ba=-1; for(const c of f.geometry.coordinates){const pf={type:'Feature',geometry:{type:'Polygon',coordinates:c}};const a=d3.geoArea(pf);if(a>ba){ba=a;best=pf}} return best }
for (const f of feats) { const n = f.properties.name, d = path(f); if (!d) continue;
  if (REP.includes(n)) out.cent[n] = proj(d3.geoCentroid(mainland(f)));
  if (REP.includes(n)) out.rep[n] = { d }; else { out.named[n] = d; } }
for (const [k, v] of Object.entries(PTS)) out.pts[k] = proj(v);
fs.writeFileSync(`../map_data_${name}.js`, 'window.MAP=' + JSON.stringify(out) + ';');
console.log(name, Object.keys(out.rep).length, 'rep', Object.keys(out.named).length, 'neigh', (fs.statSync(`../map_data_${name}.js`).size/1e6).toFixed(1)+'MB');
