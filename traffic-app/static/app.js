document.addEventListener('DOMContentLoaded', function () {
    const initialSubmitButton = document.getElementById('submitInitial');
    initialSubmitButton.addEventListener('click', validateInitialInput);

    const submit_data = document.getElementById('submitData');
    submit_data.addEventListener('click', submitData);
});

function validateInitialInput() {
    const nodes = document.getElementById('nodes').value;
    const edges = document.getElementById('edges').value;
    const emergencyCars = document.getElementById('emergencyCars').value;
    const normalCars = document.getElementById('normalCars').value;

    if (!nodes || !edges || !emergencyCars || !normalCars) {
        alert('Please fill out all the details');
        return;
    }
    createEdgeInputs(edges);
    emergencyCarInput(emergencyCars);
    normalCarInput(normalCars, emergencyCars);
    document.getElementById('submitData').style.display = 'block';

}

function createEdgeInputs(numEdges) {
    const edgeInputsContainer = document.getElementById('edgeInputsContainer');
    edgeInputsContainer.innerHTML = '';
    document.getElementById('edge-input-section').style.display = 'block';
    for (let i=0; i<numEdges; i++) {
        const edgeDiv = document.createElement('div');
        edgeDiv.className = 'data-input';
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

function emergencyCarInput(numCars){
    const car = document.getElementById('emergencyCarInput');
    car.innerHTML="";
    document.getElementById('car-section').style.display = 'block';
    for(let i = 0; i<numCars; i++){
        const carDiv = document.createElement('div');
        carDiv.className='data-input';
        carDiv.innerHTML=`
        <h4>Car ${i + 1}</h4>
            <label>From (source): </label>
            <input type="number" name="src" min="0" required>
            <label>To (destination): </label>
            <input type="number" name="dest" min="0" required>
        `;
        car.appendChild(carDiv);
    }
}
function normalCarInput(numCars, emergencyCars){
    const car = document.getElementById('normalCarInput');
    car.innerHTML="";
    for(let i = 0; i<numCars; i++){
        const carDiv = document.createElement('div');
        carDiv.className='data-input';
        carDiv.innerHTML=`
        <h4>Car ${i+parseInt(emergencyCars)+1}</h4>
            <label>From (source): </label>
            <input type="number" name="src" min="0" required>
            <label>To (destination): </label>
            <input type="number" name="dest" min="0" required>
        `;
        car.appendChild(carDiv);
    }
}

function submitEdges() {
    const form = document.getElementById('edgeForm');
    const formData = new FormData(form);
    const numEdges = document.getElementById('edges').value;
    const numCars = parseInt(document.getElementById('normalCars').value) + parseInt(document.getElementById('emergencyCars').value);
    let valid = true;
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
            congestion: parseInt(congestion),
            distance: parseInt(distance)
        });
    }
    const netData = {
        'edges':edges,
        'no_of_cars':numCars
    }
    return netData;
}

function submitCar(){
    const form = document.getElementById('car-form');
    const formData = new FormData(form);
    const numECars = parseInt(document.getElementById('normalCars').value)
    const numNCars = parseInt(document.getElementById('emergencyCars').value);
    let valid = true;
    formData.forEach((value) => {
        if (!value) {
            valid = false;
        }
    });

    if (!valid) {
        alert('Please fill out all car details');
        return;
    }
    let cars = [];
    for (let i = 0; i < numECars; i++) {
        const src = formData.getAll('src')[i];
        const dest = formData.getAll('dest')[i];
        cars.push({
            'src':parseInt(src),
            'dest':parseInt(dest),
            'type':1
        });
    }
    for (let i = 0; i < numNCars; i++) {
        const src = formData.getAll('src')[i+numECars];
        const dest = formData.getAll('dest')[i+numECars];
        cars.push({
            'src':parseInt(src),
            'dest':parseInt(dest),
            'type':0
        });
    }
    const carData = {
        src_dest : cars
    }
    return carData;
}

async function submitData(){
    const netData = submitEdges()
    const carData = submitCar();
    const finalData =  {
        'edges' : netData.edges,
        'no_of_cars':netData.no_of_cars,
        'src_dest':carData.src_dest
    }

    //calling the server to find the paths
    const response = await fetch('/dome', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(finalData)
    });

    // Wait for the POST request to finish and redirect to results page
    if (response.ok) {
        window.location.href = '/results'; // Redirect to results page after processing
    }

}