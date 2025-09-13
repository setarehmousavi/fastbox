document.addEventListener("DOMContentLoaded", function () {
  function loadCities(provinceIdField, cityIdField) {
    const provinceSelect = document.getElementById(provinceIdField);
    const citySelect = document.getElementById(cityIdField);

    provinceSelect.addEventListener("change", function () {
      const provinceName = this.options[this.selectedIndex].text;
      citySelect.innerHTML = '<option value="">-- انتخاب شهر --</option>';
      const province = locations.find(p => p.province === provinceName);
      if (!province) return;
      province.cities.forEach(city => {
        const option = document.createElement("option");
        option.value = city;
        option.textContent = city;
        citySelect.appendChild(option);
      });
    });
  }

  loadCities("id_origin_province", "id_origin_city");
  loadCities("id_destination_province", "id_destination_city");
});
