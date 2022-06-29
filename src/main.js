import {createApp} from 'vue'
import "../index.css"

function sample(array) {
    return array[Math.floor(Math.random() * array.length)];
}

createApp({
    data() {
        return {
            lastIncorrect: false,
            lastCorrect: false,
            asking: true,
            correct: 0,
            incorrect: 0,
            turtest: {
                subreddit: "Europe",
                leftpost: {
                    isHuman: false,
                    title: "",
                    text: "",
                },
                rightpost: {
                    isHuman: false,
                    title: "",
                    text: ""
                }
            }
        }
    },
    methods: {
        select(event) {
            if (!this.asking) {
                this.loadTest()
                this.lastCorrect = false;
                this.lastIncorrect = false;
            } else {
                let buttonId = event.target.id
                if ((buttonId === "left" && this.turtest.leftpost.isHuman)
                    || (buttonId === "right" && this.turtest.rightpost.isHuman)) {
                    this.correct += 1;
                    this.lastCorrect = true;
                } else {
                    this.incorrect += 1;
                    this.lastIncorrect = true;
                }
            }
            this.asking = !this.asking
        },
        loadTest() {
            console.log(window.location + "turtests.json")
            console.log("http://" + window.location.host + window.location.pathname + "turtests.json")
            let url = window.location.protocol + "//" + window.location.host + window.location.pathname + "turtests.json";
            fetch(url).then(response => response.json()).then(json => {
                let test = sample(json)
                this.turtest.subreddit = test.subreddit
                console.log(test)
                let human, ai;
                human = {
                    title: test.human.title,
                    text: test.human.text,
                    isHuman: true
                }
                ai = {
                    title: test.ai.title,
                    text: test.ai.text,
                    isHuman: false
                }
                if (Math.random() > 0.5) {
                    this.turtest.leftpost = human
                    this.turtest.rightpost = ai
                } else {
                    this.turtest.leftpost = ai
                    this.turtest.rightpost = human

                }
            })
        }
    },
    beforeMount() {
        this.loadTest()
    }
}).mount('#app')