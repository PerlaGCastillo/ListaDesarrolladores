const devForm = document.querySelector('#devForm')

let devs = []
let editing = false
let devId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/developers');
    const data = await response.json()
    devs = data
    renderDev(devs)
});

devForm.addEventListener('submit', async (e) => {
    e.preventDefault()

    const name =  devForm['name'].value
    const age = devForm['age'].value
    const languages = devForm['languages'].value

    if(!editing) {
        const response = await fetch('/developers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                age,
                languages,
            }),
        })

        const data = await response.json()
        devs.push(data)
        renderDev(devs);
    } else {
       const response = await fetch(`/developers/${devId}`, {
        method:"PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name,
            age,
            languages,
          }),
        });
        const updateDev = await response.json();

        devs = devs.map(dev => dev.id === updateDev.id ? updateDev : dev);
        console.log(devs)
        renderDev(devs);

        editing = false
        devId = null
    }

    //renderDev(devs);
    devForm.reset();
});

function renderDev(devs) {
    const devList = document.querySelector('#devList')
    devList.innerHTML = ''

    devs.forEach(dev => {
        const devItem = document.createElement('tr')
        devItem.innerHTML= `
                    <td class="text-center"> ${dev.id}</th>
                    <td> ${dev.name}</td>
                    <td class="text-center">${dev.age}</td>
                    <td class="text-center" >${dev.languages}</td>
                    <td>
                     <div class="d-flex justify-content-around align-items-center">
                        <button class="btn-edit btn btn-primary btn-sm"> Editar</button>
                        <button class="btn-delete btn btn-danger btn-sm"> Eliminar</button>
                    </div>
                    </td>
        `

        const deleteBtn = devItem.querySelector('.btn-delete')
        deleteBtn.addEventListener('click', async (e) => {
            const response = await fetch(`/developers/${dev.id}`, {
                method: 'DELETE',
            })

            const data = await response.json()

            devs = devs.filter((dev) => dev.id !== data.id)
            renderDev(devs)
        })
        devList.appendChild(devItem)

        const editBtn = devItem.querySelector('.btn-edit')
        editBtn.addEventListener('click', async (e) => {
            const response = await fetch(`/developers/${dev.id}`)
            const data = await response.json()

            devForm['name'].value = data.name;
            devForm['age'].value = data.age;
            devForm['languages'].value = data.languages;

            editing = true;
            devId = data.id;
        });
        //devList.appendChild(devItem)
    });
}
