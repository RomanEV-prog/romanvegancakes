// Logika povpraševanja: polja sledijo izbiri »Kaj naročate«, rok prevzema takoj opozori stranko.
// Končno ponudbo (ceno, rok, izvedljivost) potrdi Roman.
(function () {
  var form = document.getElementById('order-form');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var type = $('vrsta'), size = $('kosi'), flavor = $('okus'), cream1 = $('krema1'), cream2 = $('krema2');
  var sponge = $('biskvit'), decoration = $('dekoracija'), inscription = $('napis'), allergens = $('alergeni');
  var date = $('datum'), hint = $('datum-hint'), warn = $('datum-opozorilo');
  var boxFlavor = $('polje-okus'), boxCreams = $('polje-kreme'), boxSponge = $('polje-biskvit'), boxInscription = $('polje-napis');
  var boxPieces = $('polje-kosi'), boxPicture = $('polje-slika'), boxSize = size.parentNode, piece1 = $('rez1'), piece1n = $('rez1n');
  var flavorHint = $('okus-hint');

  var V = {
    ponudba: 'Torta iz ponudbe (izbran okus)',
    narocilo: 'Torta po naročilu (sestavim sam)',
    bg: 'Torta brez glutenskih sestavin',
    presna: 'Presna torta',
    pecivo: 'Rezine / pecivo (po kosih)',
    dogodek: 'Več tort / dogodek',
    drugo: 'Drugo / vprašanje'
  };
  var GF_SPONGE = 'Brez glutenskih sestavin';
  var gfFlavors = ['', 'Čokoladna', 'Malina čokolada', 'Bounty (kokos)', 'Pistacija', 'Svetujte mi'];

  // Skrito polje se ne pošlje (disabled), da v e-pošti ni praznih ali nesmiselnih vrstic.
  function show(box, on) {
    if (!box) return;
    box.hidden = !on;
    Array.prototype.forEach.call(box.querySelectorAll('select,input,textarea'), function (el) { el.disabled = !on; });
  }

  function pad(n) { return String(n).padStart(2, '0'); }
  function isoLocal(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function slDate(d) { return d.getDate() + '. ' + (d.getMonth() + 1) + '. ' + d.getFullYear(); }
  function parseLocal(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }

  function minDays() {
    var days = 10;
    // Vsaka torta 10 dni; samo dogodek ali več tort 21 dni (Roman, 13. 10. 2026).
    if (type.value === V.dogodek || size.value === 'Več kosov (po dogovoru)') days = 21;
    return days;
  }

  // Varovalka za rok: opozori takoj ob vnosu datuma in prepreči oddajo prekratkega roka.
  function checkDate() {
    var question = type.value === V.drugo;
    date.required = !question;
    if (question) {
      date.removeAttribute('min');
      hint.textContent = '(neobvezno za vprašanja)';
      date.setCustomValidity(''); date.classList.remove('je-napaka'); warn.hidden = true;
      return;
    }
    var days = minDays();
    var min = new Date(); min.setHours(0, 0, 0, 0); min.setDate(min.getDate() + days);
    date.min = isoLocal(min);
    hint.textContent = '(najmanj ' + days + ' dni vnaprej, od ' + slDate(min) + ')';
    if (date.value && parseLocal(date.value) < min) {
      var msg = 'Za ta datum naročila ne morem sprejeti: za izbrano vrsto potrebujem najmanj ' + days + ' dni, najzgodnejši prevzem je ' + slDate(min) + '. Za nujno naročilo me pokličite na 040 758 582.';
      warn.textContent = msg; warn.hidden = false;
      date.classList.add('je-napaka');
      date.setCustomValidity('Najzgodnejši prevzem je ' + slDate(min) + '.');
    } else {
      warn.hidden = true; date.classList.remove('je-napaka'); date.setCustomValidity('');
    }
  }

  function update() {
    var t = type.value;
    var cake = t === V.ponudba || t === V.narocilo || t === V.bg;
    var gf = t === V.bg || allergens.value === 'Brez glutenskih sestavin';

    // Okus: torta iz ponudbe in BG torta; torta po naročilu ima kreme namesto okusa.
    show(boxFlavor, t === V.ponudba || t === V.bg || t === V.presna || t === V.dogodek || t === '');
    // Rezine: okusi in število kosov po vrsticah namesto velikosti torte.
    show(boxPieces, t === V.pecivo);
    show(boxSize, t !== V.pecivo);
    piece1.required = t === V.pecivo; piece1n.required = t === V.pecivo;
    show(boxCreams, t === V.narocilo);
    show(boxSponge, t === V.ponudba || t === V.narocilo || t === '');
    flavor.required = t === V.ponudba || t === V.bg;
    cream1.required = t === V.narocilo;
    if (flavorHint) {
      flavorHint.textContent = t === V.bg ? 'Brez glutenskih sestavin pripravljam čokoladno, čokolada–malino, Bounty in pistacijo, do 10 kosov.'
        : t === V.presna ? 'Presne torte po dogovoru; želeni okus opišite v sporočilu.'
        : t === V.dogodek ? 'Izberite okus ali želje opišite v sporočilu.'
        : 'Torta iz ponudbe ima kremo po receptu, izberete le biskvit.';
    }

    // BG: samo štirje okusi, največ 10 kosov, biskvit je fiksen.
    Array.prototype.forEach.call(flavor.options, function (o) { if (o.value) o.disabled = gf && gfFlavors.indexOf(o.value) < 0; });
    if (flavor.selectedOptions[0] && flavor.selectedOptions[0].disabled) flavor.value = '';
    if (gf && !boxSponge.hidden) sponge.value = GF_SPONGE;
    Array.prototype.forEach.call(sponge.options, function (o) { o.disabled = gf && o.value !== GF_SPONGE; });
    var gfSize = gf || sponge.value === GF_SPONGE;
    Array.prototype.forEach.call(size.options, function (o) {
      if (!o.value) return;
      o.disabled = gfSize && ['12 kosov', 'Več kosov (po dogovoru)', 'Rezine po kosih'].indexOf(o.value) >= 0;
    });
    if (size.selectedOptions[0] && size.selectedOptions[0].disabled && size.value) size.value = '';
    if (!cake && sponge.value === GF_SPONGE && t !== '') sponge.value = '';

    // Krema 2 ne sme biti enaka kremi 1.
    Array.prototype.forEach.call(cream2.options, function (o) { if (o.value) o.disabled = o.value === cream1.value && o.value !== 'Svetujte mi'; });
    if (cream2.selectedOptions[0] && cream2.selectedOptions[0].disabled) cream2.value = '';

    // Napis: polje za besedilo samo, ko je izbran; jedilna slika: priloga kar v obrazcu.
    show(boxInscription, decoration.value.indexOf('Napis') === 0);
    show(boxPicture, decoration.value.indexOf('edilna slika') >= 0);

    checkDate();
  }

  [type, size, flavor, cream1, cream2, sponge, decoration, allergens].forEach(function (f) { f.addEventListener('change', update); });
  date.addEventListener('input', checkDate);
  date.addEventListener('change', checkDate);
  form.addEventListener('submit', function (e) {
    checkDate();
    if (!date.validity.valid) { e.preventDefault(); date.focus(); date.reportValidity(); }
  });
  update();
})();
