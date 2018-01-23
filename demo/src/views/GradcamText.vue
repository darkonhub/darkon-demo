<template>
<section class="section">
  <div class="container">
    <h1 class="title is-1">Grad-CAM for text</h1>
    <p>
      This demo shows an example usage of Grad-CAM function of Darkon package. If you select pretrained network and a specific test sample, you can see Grad CAM for both negative prediction and positive prediction. It indicates the words that affects the decision.
    </p>
  </div>

  <div class="container" id="select-network">
    <hr>
    <p class="title is-3">1. Select Network</p>
    <aside class="menu content">
    <ul class="menu-list">
      <li v-for="aModel, idx in trainModels" :key="idx">
        <a :class="aModel.selected ? 'is-active' : null" v-scroll-to="'#select-data'" @click="onNext(1, {modelIdx:idx})">{{ aModel.title }}</a>
      </li>
    </ul>
    </aside>
  </div>

  <div class="container" id="select-data">
    <div v-if="showcaseStep>=1">
      <hr>
      <p class="title is-3">2. Select test data</p>
      <aside class="menu content">
      <ul class="menu-list">
        <li v-for="item, idx in selectedDatabase" :key="idx">
          <a :class="item.selected ? 'is-active' : null" v-scroll-to="'#report-gradcam'" @click="onNext(2, {dataIdx:idx})" >
            <b>{{ item.pred }}:</b> {{ item.src }}
          </a>
        </li>
      </ul>
      </aside>
    </div>
  </div>

  <div class="container" id="report-gradcam">
    <div v-if="showcaseStep>=2">
      <hr>
      <p class="title is-3">3. Gradcam Result</p>

      <table class="table is-fullwidth ">
        <tbody>
          <tr>
            <th>input</th>
            <td>
              <span v-for="item, idx in selectedDatabase[dataIdx].retGradcam" :key="idx">
                {{ item[0] }}
              </span>
            </td>
          </tr>
          <tr class="result">
            <th :class="selectedDatabase[dataIdx].pred == 'pos' ? 'pred' : null">
              positive<br>decision
            </th>
            <td>
              <span v-for="item, idx in selectedDatabase[dataIdx].retGradcam" :key="idx" :style="positiveTextStyle(item[1])">
                {{ item[0] }}
              </span>
            </td>
          </tr>
          <tr class="result">
            <th :class="selectedDatabase[dataIdx].pred == 'neg' ? 'pred' : null">
              negative<br>decision
            </th>
            <td>
              <span v-for="item, idx in selectedDatabase[dataIdx].retGradcam" :key="idx" :style="negativeTextStyle(item[2])">
                {{ item[0] }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="container" id="tail">
    <div v-show="showcaseStep>=2">
      <br>
      <button class="button is-danger" v-scroll-to="'#select-network'" @click="gotoTop">Go to the first step</button>
    </div>
  </div>

</section>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      showcaseStep: 0,
      modelIdx: 0,
      dataIdx: 0,
      totalDatabase: {},
      selectedDatabase: null,
      trainModels: [
        {title: 'CNN, Text sentiment classification', name: 'text', selected: false}
      ]
    }
  },

  mounted () {
    let self = this

    axios.get('/static/gradcam_text_database.json')
    .then(function (response) {
      let database = response.data

      let textDatabase = []
      for (let rowIdx = 0; rowIdx < database.length; rowIdx++) {
        let item = database[rowIdx]
        let aData = {
          selected: false,
          src: item['src'],
          retGradcam: item['ret_gradcam'],
          pred: item['pred']
        }
        textDatabase.push(aData)
      }

      self.totalDatabase['text'] = textDatabase
    })
    .catch(function (error) {
      console.log(error)
    })
  },

  methods: {
    onNext (nextStep, meta) {
      switch (nextStep) {
        case 1:
          this.modelIdx = meta.modelIdx
          this.clearSelectedModel()
          this.clearSelectedData()
          this.trainModels[meta.modelIdx].selected = true
          this.selectedDatabase = this.totalDatabase[this.trainModels[meta.modelIdx].name]
          break
        case 2:
          this.dataIdx = meta.dataIdx
          this.clearSelectedData()
          let selectedData = this.selectedDatabase[this.dataIdx]
          selectedData.selected = true
          break
      }
      this.showcaseStep = nextStep
    },

    clearSelectedModel () {
      for (let idx = 0; idx < this.trainModels.length; idx++) {
        this.trainModels[idx].selected = false
      }
    },

    clearSelectedData () {
      for (let key in this.totalDatabase) {
        let database = this.totalDatabase[key]
        for (let dataIdx = 0; dataIdx < database.length; dataIdx++) {
          database[dataIdx].selected = false
        }
      }
    },

    gotoTop () {
      this.clearSelectedModel()
      this.clearSelectedData()
      this.showcaseStep = 0
    },

    positiveTextStyle (alpha) {
      return 'color: rgba(255, 99, 132, ' + alpha + ');'
    },

    negativeTextStyle (alpha) {
      return 'color: rgba(54, 162, 235, ' + alpha + ');'
    }
  }
}
</script>

<style lang="sass" scoped>
@import "../assets/sass/main.scss"

.section
  text-align: left

#select-data
  img
    width: 18.5%
    margin: 2px

  .img-selectable
    border: 1px solid #000

  .img-selectable:hover
    border: 5px solid darken($turquoise, 10)

  .img-selected
    border: 5px solid $turquoise

#report-gradcam
  text-align: center

  th
    vertical-align: middle
    padding: 0.4em
    font-weight: normal
    font-size: 1em
    text-align: right

  td
    vertical-align: middle
    padding: 0.4em
    font-weight: bold
    font-size: 1.5em

  .result td
    border: 1px solid
    border-radius: $radius-small
    background-color: #000

  .result .pred
    background-color: $turquoise


</style>
