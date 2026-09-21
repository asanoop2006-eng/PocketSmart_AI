document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const budget = form.querySelector('[name="budget"]');

            if (budget && (budget.value.trim() === "" || Number(budget.value) <= 0)) {

                event.preventDefault();

                alert("Please enter a valid budget greater than ₹0.");

                budget.focus();

                return;
            }


            const guests = form.querySelector('[name="guests"]');

            if (guests && (guests.value.trim() === "" || Number(guests.value) <= 0)) {

                event.preventDefault();

                alert("Please enter a valid number of guests.");

                guests.focus();

                return;
            }


            const quantityFields = ["lights", "fans", "tables"];

            for (let fieldName of quantityFields) {

                const field = form.querySelector(`[name="${fieldName}"]`);

                if (field && (field.value.trim() === "" || Number(field.value) < 0)) {

                    event.preventDefault();

                    alert("Please enter valid quantities for all items.");

                    field.focus();

                    return;
                }
            }

        });

    });

});