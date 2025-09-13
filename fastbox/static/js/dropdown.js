document.addEventListener("DOMContentLoaded", () => {
    // Get form fields
    const originProvince = document.getElementById("id_origin_province");
    const originCity = document.getElementById("id_origin_city");
    const destProvince = document.getElementById("id_destination_province");
    const destCity = document.getElementById("id_destination_city");

    // Initialize Choices.js on each select
    const originProvinceChoice = new Choices(originProvince, { searchEnabled: true });
    const originCityChoice = new Choices(originCity, { searchEnabled: true });
    const destProvinceChoice = new Choices(destProvince, { searchEnabled: true });
    const destCityChoice = new Choices(destCity, { searchEnabled: true });

    // Function to update cities based on selected province
    function updateCities(provinceSelect, cityChoice) {
        const cities = locations[provinceSelect.value] || [];
        const choicesArray = cities.map(city => ({ value: city, label: city }));
        cityChoice.clearChoices();
        cityChoice.setChoices(choicesArray, 'value', 'label', true);
    }

    // Event listeners for province change
    originProvince.addEventListener("change", () => updateCities(originProvince, originCityChoice));
    destProvince.addEventListener("change", () => updateCities(destProvince, destCityChoice));
});
