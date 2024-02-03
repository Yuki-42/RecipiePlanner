// Wait for the window to load before running the script
window.onload = function () {
    const sortableList = document.getElementById("items");
    let draggedItem = null;
    // Script.js


    sortableList.addEventListener(
        "dragstart",
        (e) => {
            draggedItem = e.target;
            setTimeout(() => {
                e.target.style.display =
                    "none";
            }, 0);
        });

    sortableList.addEventListener(
        "dragend",
        (e) => {
            setTimeout(() => {
                e.target.style.display = "";
                draggedItem = null;
            }, 0);
        });

    sortableList.addEventListener(
        "dragover",
        (e) => {
            e.preventDefault();
            const afterElement =
                getDragAfterElement(
                    sortableList,
                    e.clientY);
            const currentElement =
                document.querySelector(
                    ".dragging");
            if (afterElement == null) {
                sortableList.appendChild(
                    draggedItem
                );
            } else {
                sortableList.insertBefore(
                    draggedItem,
                    afterElement
                );
            }
        });

    const getDragAfterElement = (
        container, y
    ) => {
        const draggableElements = [
            ...container.querySelectorAll(
                "li:not(.dragging)"
            ),];

        return draggableElements.reduce(
            (closest, child) => {
                const box =
                    child.getBoundingClientRect();
                const offset =
                    y - box.top - box.height / 2;
                if (
                    offset < 0 &&
                    offset > closest.offset) {
                    return {
                        offset: offset,
                        element: child,
                    };
                } else {
                    return closest;
                }
            },
            {
                offset: Number.NEGATIVE_INFINITY,
            }
        ).element;
    };
}

function checkboxClick(checkbox) {
    // Get the parent list item
    const listItem = checkbox.parentElement.parentElement;

    // If the checkbox is checked, add the class 'completed' to the list item and move the list item to the bottom of the list
    if (checkbox.checked) {
        listItem.classList.add('completed');
        listItem.parentElement.appendChild(listItem);
    } else {
        // If the checkbox is not checked, remove the class 'completed' from the list item and move the list item to the top of the list
        listItem.classList.remove('completed');
        listItem.parentElement.prepend(listItem);
    }
}

function showRecipies(){
    console.log("test")
    // Show the popup
    document.getElementById("recipies-popup").style.display = "block";
    // Play the slide animation
    document.getElementById("recipies-popup").classList.add("slide-up");

}

