

let container = document.getElementById('table');

let data = [];

let hot = new Handsontable(container, {
  data: data,
  rowHeaders: true,
  colHeaders: true,
  filters: true,
  dropdownMenu: true
});

async function getData() {
  console.log('getting data!');
  let resp = await fetch('http://localhost:7000/data.json');
  hot.loadData(await resp.json());
}

async function saveData() {
  console.log('saving data!');
  console.log(JSON.stringify(hot.getData()));
  return await fetch('http://localhost:7000/save', {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(hot.getData())
  })
}

let load = document.getElementById('load');
let save = document.getElementById('save');

load.addEventListener("click", () => getData());
save.addEventListener("click", () => saveData());