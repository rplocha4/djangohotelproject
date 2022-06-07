const btn = document.getElementById('pay-btn');
const btn2 = document.getElementById('lds-ring');

btn.addEventListener('click', () => {
    // 👇️ hide button
    btn.style.display = 'none';
    console.log("asdsa")

    // 👇️ show div

    btn2.style.display = 'inline-block;';
});