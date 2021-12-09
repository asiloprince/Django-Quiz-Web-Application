'use strict'

const url = window.location.href
let data
const formBox = document.getElementById('quiz-box')
const resultBox = document.getElementById('result-box')
console.log(resultBox)
const scoreBox = document.getElementById('score-box')
console.log(scoreBox)
console.log(formBox)
const timerBox = document.getElementById('timerbox')

const activateTime = (time) => {

	if (time.toString().length < 2) {
		timerBox.innerHTML += `<b> 0 ${time} : 00</b>`
	} else {
		timerBox.innerHTML += `<b> ${time} : 00</b>`
	}

	let minutes = time - 1
	let seconds = 60
	let displayMinutes
	let displaySeconds


	const timer = setInterval(() => {

		seconds--
		if (seconds < 0) {
			seconds = 59
			minutes--
		}

		if (minutes.toString().length < 2) {
			displayMinutes = '0' + minutes
		}
		else {
			displayMinutes = minutes
		}


		if (seconds.toString().length < 2) {
			displaySeconds = '0' + seconds
		}
		else {
			displaySeconds = seconds
		}

		if (minutes === 0 && seconds === 0) {
			console.log("It's over haha")
			alert("Over")
			clearInterval(timer)
			sendData()
		}

		timerBox.innerHTML = `<b>${displayMinutes} : ${displaySeconds}`

	}, 1000);
}


$.ajax({


	method: "GET",
	url: `${url}data`,

	success: function (response) {
		data = response.data
		data.forEach(el => {

			for (const [questions, answers] of Object.entries(el)) {

				formBox.innerHTML += `

					<hr>
					<div class="mb-2">
						<b>${questions}</b>
					</div>

				`

				answers.forEach(answer => {
					formBox.innerHTML += `


						<div>
						<input type="radio" name="${questions}" class="ans" id="${questions} - ${answer}" value="${answer}">
						<label for="${questions}"> ${answer} </label>
						</div>


					`
				});
			}

		});
		activateTime(response.time)
	},
	error: function (error) {
		console.log(error)
	}


})

const quizForm = document.getElementById('form-quiz')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {

	const elements = [...document.getElementsByClassName('ans')]
	const data = {}
	data['csrfmiddlewaretoken'] = csrf[0].value
	elements.forEach(el => {

		if (el.checked) {
			data[el.name] = el.value
		}
		else {

			if (!data[el.name]) {
				data[el.name] = null
			}
		}
	});

	$.ajax({

		type: 'POST',
		url: `${url}save/`,
		data: data,
		success: function (response) {

			const results = response.results;
			console.log(results);
			quizForm.classList.add('not-visible');
			scoreBox.innerHTML = `${response.passed ? "Congratulations" : "Oops"} Your result is ${response.score.toFixed(2)}`
			results.forEach(res => {

				const resDiv = document.createElement("div")
				for (const [question, resp] of Object.entries(res)) {
					console.log(question)
					console.log(resp)
					console.log("%%%%%")

					resDiv.innerHTML += question
					const cls = ['container', 'p-3', 'text-light', 'h6']
					resDiv.classList.add(...cls)

					if (resp == 'Not answered') {
						resDiv.innerHTML += 'Not Answered'
						resDiv.classList.add('bg-danger')
					}
					else {
						const correct = resp['correct_answer']
						const answer = resp['answered']

						if (answer == correct) {
							resDiv.classList.add('bg-success')
							resDiv.innerHTML += `Answered ${answer}`
						}
						else {
							resDiv.classList.add('bg-danger')

							resDiv.innerHTML += ` | Correct Answer ${correct}`
							resDiv.innerHTML += ` | Answered ${answer}`

						}

					}
				}
				const body = document.getElementsByTagName('BODY')[0]
				resultBox.append(resDiv)

			});
		},
		error: function (response) {
			console.log(response)
		}
	});

}

quizForm.addEventListener('submit', e => {
	e.preventDefault()
	sendData()
});