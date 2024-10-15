document.addEventListener('DOMContentLoaded', function () {
    const initialSubmitButton = document.getElementById('submitInitial');
    initialSubmitButton.addEventListener('click', validateInitialInput);

    const edgeSubmitButton = document.getElementById('submitEdges');
    edgeSubmitButton.addEventListener('click', submitEdges);
});

function validateInitialInput() {
    const nodes = document.getElementById('nodes').value;
    const edges = document.getElementById('edges').value;
    const emergencyCars = document.getElementById('emergencyCars').value;
    const normalCars = document.getElementById('normalCars').value;

    if (!nodes || !edges || !emergencyCars || !normalCars) {
        alert('Some error in input');
        return;
    }
    createEdgeInputs(edges);
}

function createEdgeInputs(numEdges) {
    const edgeInputsContainer = document.getElementById('edgeInputsContainer');
    edgeInputsContainer.innerHTML = '';
    document.getElementById('initial-input').style.display = 'none';
    document.getElementById('edge-input-section').style.display = 'block';
    for (let i = 0; i < numEdges; i++) {
        const edgeDiv = document.createElement('div');
        edgeDiv.className = 'edge-input';
        edgeDiv.innerHTML = `
            <h4>Edge ${i + 1}</h4>
            <label>From (u): </label>
            <input type="number" name="u" min="0" required>
            <label>To (v): </label>
            <input type="number" name="v" min="0" required><br>
            <label>Congestion: </label>
            <input type="number" name="congestion" min="0" required>
            <label>Distance: </label>
            <input type="number" name="distance" min="0" required><br>
        `;
        edgeInputsContainer.appendChild(edgeDiv);
    }
}

function submitEdges() {
    const form = document.getElementById('edgeForm');
    const formData = new FormData(form);
    const numEdges = document.getElementById('edges').value;

    let valid = true;
    console.log(formData)
    formData.forEach((value) => {
        if (!value) {
            valid = false;
        }
    });

    if (!valid) {
        alert('Please fill out all edge details');
        return;
    }
    let edges = [];
    for (let i = 0; i < numEdges; i++) {
        const u = formData.getAll('u')[i];
        const v = formData.getAll('v')[i];
        const congestion = formData.getAll('congestion')[i];
        const distance = formData.getAll('distance')[i];

        edges.push({
            u: parseInt(u),
            v: parseInt(v),
            attributes: {
                congestion: parseInt(congestion),
                distance: parseInt(distance)
            }
        });
    }

    // Log the final JSON object to console (or send to server)
    //console.log(edges);
    //Convert to JSON object with correct format
    const jsonEdges = edges.map(edge => {
        return `(${edge.u}, ${edge.v}, {'congestion': ${edge.attributes.congestion}, 'distance': ${edge.attributes.distance}})`;
    });

    //console.log("Formatted Edges:", jsonEdges.join(",\n"));
    alert('Edges have been submitted! Check console for JSON object.');
}
