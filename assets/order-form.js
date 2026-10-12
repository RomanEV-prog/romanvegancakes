// Roki in velikosti sledijo izbiri v povpraševanju; končno ponudbo potrdi Roman.
(function () {
  var form = document.getElementById('order-form');
  if (!form) return;
  var type = document.getElementById('vrsta');
  var size = document.getElementById('kosi');
  var flavor = document.getElementById('okus');
  var sponge = document.getElementById('biskvit');
  var decoration = document.getElementById('dekoracija');
  var allergens = document.getElementById('alergeni');
  var date = document.getElementById('datum');
  var hint = document.getElementById('datum-hint');
  var gfFlavors = ['', 'Čokolada', 'Malina čokolada', 'Bounty (kokos)', 'Pistacija', 'Svetujte mi'];

  function update() {
    var gfRequired = type.value === 'Brezglutenska torta' || allergens.value === 'Brez glutena';
    // Izrecna izbira brezglutenske torte zahteva ustrezen biskvit.
    if (gfRequired) sponge.value = 'Brezglutenski';
    var gf = gfRequired || sponge.value === 'Brezglutenski';
    Array.from(sponge.options).forEach(function (option) {
      option.disabled = gfRequired && option.value !== 'Brezglutenski';
    });
    Array.from(size.options).forEach(function (option) {
      if (!option.value) return;
      option.disabled = gf && ['12 kosov', 'Več kosov (po dogovoru)', 'Rezine po kosih'].includes(option.value);
    });
    if (size.selectedOptions[0] && size.selectedOptions[0].disabled && size.value) size.value = '';
    Array.from(flavor.options).forEach(function (option) {
      if (!option.value) return;
      option.disabled = gf && !gfFlavors.includes(option.value);
    });
    if (flavor.selectedOptions[0] && flavor.selectedOptions[0].disabled && flavor.value) flavor.value = '';

    var days = 10;
    if (gf || type.value === 'Torta z jedilno sliko' || type.value === 'Poseben okus po dogovoru' || decoration.value.startsWith('Jedilna slika')) days = 14;
    if (type.value === 'Več tort / dogodek' || size.value === 'Več kosov (po dogovoru)') days = 21;
    var question = type.value === 'Drugo / vprašanje';
    date.required = !question;
    if (question) {
      date.removeAttribute('min');
      hint.textContent = '(neobvezno za vprašanja)';
    } else {
      var min = new Date();
      min.setDate(min.getDate() + days);
      // Lokalni koledarski datum, brez premika zaradi UTC.
      date.min = min.getFullYear() + '-' + String(min.getMonth() + 1).padStart(2, '0') + '-' + String(min.getDate()).padStart(2, '0');
      hint.textContent = '(najmanj ' + days + ' dni vnaprej)';
    }
  }
  [type, size, flavor, sponge, decoration, allergens].forEach(function (field) { field.addEventListener('change', update); });
  update();
})();
