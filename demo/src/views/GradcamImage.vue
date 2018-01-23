<template>
<section class="section">
  <div class="container">
    <h1 class="title is-1">Grad-CAM for image</h1>
    <p>
      This demo shows an example usage of Grad-CAM function of Darkon package. If you select pretrained network and a specific test sample, you can see top-5 prediction result and Grad CAM and Guided Grad CAM for the prediction, which indicate the location and feature of input that affect the decision.
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
      <a v-for="item, idx in selectedDatabase" @click="onNext(2, {dataIdx:idx})" v-scroll-to="'#report-gradcam'" :key="idx">
        <img :src="item.src" :class="item.selected?'img-selected': null" class="img-selectable">
      </a>
    </div>
  </div>

  <div class="container" id="report-gradcam">
    <div v-if="showcaseStep>=2">
      <hr>
      <p class="title is-3">3. Gradcam Result</p>
      <div class="my-columns">
        <p class="subtitle is-4">Gradcam</p>
        <div class="my-column" v-for="item, idx in selectedDatabase[dataIdx].retGradcam" :key="idx">
          <img :src="item[0]">
          <p>{{ item[1] }} ({{ item[2].toFixed(3) }})</p>
        </div>
      </div>
      <div class="my-columns">
        <p class="title is-4">Guided gradcam</p>
        <div class="my-column" v-for="item, idx in selectedDatabase[dataIdx].retGuidedGradcam" :key="idx">
          <img :src="item[0]">
          <p>{{ item[1] }} ({{ item[2].toFixed(3) }})</p>
        </div>
      </div>
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
        {title: 'Resnet 50, ImageNet dataset', name: 'resnet', selected: false},
        {title: 'VGG 16, ImageNet dataset', name: 'vgg', selected: false}
      ],
      chartData: {
        datasets: [
          {
            backgroundColor: 'rgba(255, 99, 132, 0.4)',
            borderColor: 'rgba(255, 99, 132, 1.0)',
            borderWidth: 1,
            data: null
          },
          {
            backgroundColor: 'rgba(54, 162, 235, 0.4)',
            borderColor: 'rgba(54, 162, 235, 1.0)',
            borderWidth: 1,
            data: null
          }
        ],
        labels: []
      }
    }
  },

  mounted () {
    let self = this
    axios.get('/static/gradcam_resnet_database.json')
    .then(function (response) {
      let database = response.data

      let resnetDatabase = []
      for (let rowIdx = 0; rowIdx < database.length; rowIdx++) {
        let item = database[rowIdx]
        let aData = {
          selected: false,
          src: item['src'],
          retGradcam: item['ret_gradcam'],
          retGuidedGradcam: item['ret_guided_gradcam']
        }
        resnetDatabase.push(aData)
      }

      self.totalDatabase['resnet'] = resnetDatabase
    })
    .catch(function (error) {
      console.log(error)
    })

    axios.get('/static/gradcam_vgg_database.json')
    .then(function (response) {
      let database = response.data

      let vggDatabase = []
      for (let rowIdx = 0; rowIdx < database.length; rowIdx++) {
        let item = database[rowIdx]
        let aData = {
          selected: false,
          src: item['src'],
          retGradcam: item['ret_gradcam'],
          retGuidedGradcam: item['ret_guided_gradcam']
        }
        vggDatabase.push(aData)
      }

      self.totalDatabase['vgg'] = vggDatabase
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
    }
  }
}
</script>

<style lang="sass" scoped>
@import "../assets/sass/main.scss";

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
  .my-column
    display: inline-block
    width: 18.5%
    border: 1px solid #000
    margin: 2px 2px 10px 2px
    background-color: #000
    color: $white-ter

  img
    width: 100%

  p
    width: 100%
    text-align: center

</style>
