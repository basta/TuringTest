import { createApp } from 'vue'

function sample(array) {
  return array[Math.floor(Math.random() * array.length)];
}

createApp({
  data() {
    return {
      asking: true,
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
    select(event){
      if (!this.asking){
        this.loadTest()
      }
      this.asking = !this.asking
    },
    loadTest(){
      fetch("/turtests.json").then( response => response.json()).then(json => {
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
        if (Math.random() > 0.5){
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