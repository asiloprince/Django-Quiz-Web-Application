'use strict'


const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

console.log(startBtn)

const url = window.location.href

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {



	const pk = modalBtn.getAttribute('data-pk')
	const name = modalBtn.getAttribute('data-quiz')
	const ques = modalBtn.getAttribute('data-questions')
	const diff = modalBtn.getAttribute('data-difficulty')
	const time = modalBtn.getAttribute('data-time')
	const pass = modalBtn.getAttribute('data-pass')


	console.log(name)

	modalBody.innerHTML = `

	<div class="h5" mb-3"> Let's go for <b>${name}</b></div>
	<div class="text-muted">
	<ul>

		<li> Difficulty: <b> ${diff} </b> </li>
		<li> Number Of Questions: <b> ${ques} </b> </li>
		<li> Time: <b> ${time} Minutes </b> </li>
		<li> Required Score:  <b> ${pass} </b> </li>


	</ul>
	</div>


	`

	startBtn.addEventListener('click', () => {

		window.location.href = url + pk

	})







}))