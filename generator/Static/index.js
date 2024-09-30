
const Main = () => {
    document.querySelector('.bars--div').style.display = 'flex';
    document.querySelector('.userDiv').style.display = 'none';

    Space1()
   
    window.addEventListener('resize', event => {
        document.querySelector('.space--2').innerHTML = window.innerWidth
    })

}

function Hide_userDiv() {
    document.querySelector('.userDiv').style.display = 'none';
}

function Space1() {
    let inputFile = document.getElementById('fileInput1')
    let fileNameField = document.querySelector('.fileBtn--fileName1')

    inputFile.addEventListener('change', (event) => {
        let name = event.target.files[0].name;
        fileNameField.innerHTML = name;
        fileNameField.style.display = 'inline-block'
        document.getElementById('ConvertBtn').style.display = "block";
        document.querySelector('.layoutBox').style.display = "flex";
        
    })
}
function userDiv_toggle() {
    let userDiv = document.querySelector('.userDiv');

    (userDiv.style.display == 'none') ? userDiv.style.display = 'flex' : userDiv.style.display = 'none';
}

function Convert_display() {
    document.getElementById('ConvertBtn').style.display = "none";
    document.getElementById('convert').style.display = "block";
}

function barsToggle() {
    let bars_div = document.querySelector('.bars--div');
    let space = document.querySelector('.space');

    if (bars_div.style.display === 'flex') 
    {
        bars_div.style.display = 'none'
        space.style.marginLeft = '30px'
        space.style.borderTopLeftRadius = '20px'
        space.style.borderBottomLeftRadius = '20px'
    }
    else 
    {
        bars_div.style.display = 'flex';
        space.style.marginLeft = '0px'
        space.style.borderTopLeftRadius = '0px'
        space.style.borderBottomLeftRadius = '0px'
    }
}

function setSpace(id) {
    let prev = document.querySelectorAll('.spaceBtn')

    prev.forEach(element => {
        if(element.classList.contains('spaceBtn--active')){
            element.classList.remove('spaceBtn--active');
            document.querySelector(`.space--${element.id}`).style.display = 'none';
        } 
    });
    
    document.getElementById(id).classList.add('spaceBtn--active')

    document.querySelector(`.space--${id}`).style.display = 'flex';


}
