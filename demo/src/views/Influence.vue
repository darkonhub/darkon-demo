<template>
<section class="section">
  <div class="container">
    <h1 class="title is-1">Influence function for image</h1>
    <p>
      This demo shows an example usage of upweighting influence function of Darkon package. If you select pertained network and a specific test sample, you can see the prediction result and helpful or harmful training samples on the prediction. Training samples are sorted by influence scores, where highest (positive) values correspond to helpful samples and lowest (negative) values correspond to harmful samples.
    </p>
  </div>

  <div class="container content" id="select-network">
    <hr>
    <p class="title is-3">1. Select Network</p>
    <ul>
      <li><a v-scroll-to="'#select-image'" @click="showcaseStep=1">Resnet 110, CIFAR-10 dataset</a></li>
    </ul>
  </div>

  <div class="container" id="select-image">
    <div v-if="showcaseStep>=1">
      <hr>
      <p class="title is-3">2. Select test image</p>
      <tabs :only-fade="false" ref="tabs" type="boxed">
        <tab-pane v-for="aClass, classIdx in targets" :label="aClass.name" :key="classIdx">
          <a v-for="item, imgIdx in aClass.images" @click="showcaseStep=2; onSelectTarget(aClass.name, imgIdx)" v-scroll-to="'#report-classification'">
            <img :src="item.src" :class="item.selected?'img-selected': ''" :key="imgIdx" class="img-selectable">
          </a>
        </tab-pane>
      </tabs>
    </div>
  </div>

  <div class="container" id="report-classification">
    <div v-show="showcaseStep>=2">
      <hr>
      <p class="title is-3">3. Classification result</p>
      <accuracy-chart :chartData="chartData" :width="400" :height="150"/>
      <br><br>
      <button class="button is-success" v-scroll-to="'#report-influence'" @click="showcaseStep=3; onSelectHelpfulSample()">Helpful samples</button>
      <button class="button is-danger" v-scroll-to="'#report-influence'" @click="showcaseStep=3; onSelectHarmfulSample()">Harmful samples</button>
    </div>
  </div>

  <div class="container" id="report-influence">
    <div v-show="showcaseStep>=3">
      <hr>
      <p class="title is-3">4. Upweighting Influence Result</p>
      <p class="subtitle is-4">{{ influenceInfo.title }}</p>
      <div class="my-columns">
        <div class="my-column" v-for="item, idx in subInfluenceInfo(0, 5)" :key="idx">
          <img :src="item[0]">
          <p>{{ item[1] }}</p>
        </div>
      </div>
      <div class="my-columns">
        <div class="my-column" v-for="item, idx in subInfluenceInfo(5, 10)" :key="idx">
          <img :src="item[0]">
          <p>{{ item[1] }}</p>
        </div>
      </div>
    </div>
  </div>

  <div class="container" id="tail">
    <div v-show="showcaseStep>=3">
      <br>
      <button class="button is-danger" v-scroll-to="'#select-network'" @click="gotoTop">Go to the first step</button>
    </div>
  </div>

</section>
</template>

<script>
import _ from 'lodash'
import {Tabs, TabPane} from 'vue-bulma-tabs'
import AccuracyChart from '@/components/AccuracyChart'

import axios from 'axios'

export default {
  components: {
    Tabs,
    TabPane,
    AccuracyChart
  },

  props: {
    classes: {
      type: Array,
      default: () => [
        'airplane',
        'automobile',
        'bird',
        'cat',
        'deer',
        'dog',
        'frog',
        'horse',
        'ship',
        'truck'
      ]
    },
    barColor: {
      type: Array,
      default: () => ['rgba(255, 99, 132, 0.4)', 'rgba(201, 203, 207, 0.4)']
    },
    barBorderColor: {
      type: Array,
      default: () => ['rgba(255, 99, 132, 1)', 'rgba(201, 203, 207, 1)']
    }
  },

  data () {
    return {
      targets: null,
      showcaseStep: 0,
      influenceInfo: {
        title: '',
        samples: null
      },
      chartData: {
        labels: this.classes,
        datasets: [
          {
            backgroundColor: null,
            borderColor: null,
            borderWidth: 1,
            data: null
          }
        ]
      },
      resultsHelpful: null,
      resultsHarmful: null,
      database: null
    }
  },

  mounted () {
    let self = this
    axios.get('/static/demo_database.json')
    .then(function (response) {
      self.database = response.data

      let targets = []
      for (let i = 0; i < self.classes.length; i++) {
        let aClass = {name: self.classes[i], images: []}
        for (let j of _.range(5)) {
          let row = self.database[i * 5 + j]
          aClass.images.push({src: '/static/test_images/' + row['key'] + '.png', selected: false})
        }
        targets.push(aClass)
      }
      self.targets = targets
    })
    .catch(function (error) {
      console.log(error)
    })
  },

  methods: {
    onSelectTarget (className, idx) {
      this.clearSelectedData()
      let classIdx = _.indexOf(this.classes, className)
      this.targets[classIdx].images[idx].selected = true

      let row = this.database[classIdx * 5 + idx]
      this.resultsHelpful = _.zip(_.map(row['helpful'], (i) => '/static/train_images/' + i + '.png'), row['helpful_meta'])
      this.resultsHarmful = _.zip(_.map(row['harmful'], (i) => '/static/train_images/' + i + '.png'), row['harmful_meta'])

      let chartData = _.clone(this.chartData)
      chartData.datasets[0].data = row.pred
      chartData.datasets[0].backgroundColor = _.map(_.range(10), (i) => i === classIdx ? this.barColor[0] : this.barColor[1])
      chartData.datasets[0].borderColor = _.map(_.range(10), (i) => i === classIdx ? this.barBorderColor[0] : this.barBorderColor[1])
      this.chartData = chartData
    },

    onSelectHelpfulSample () {
      this.influenceInfo.title = 'Helpful train samples: To decrease loss'
      this.influenceInfo.samples = this.resultsHelpful
    },

    onSelectHarmfulSample () {
      this.influenceInfo.title = 'Harmful train samples: To increase loss'
      this.influenceInfo.samples = this.resultsHarmful
    },

    subInfluenceInfo (begin, end) {
      if (!this.influenceInfo.samples) return []
      return _.slice(this.influenceInfo.samples, begin, end)
    },

    clearSelectedData () {
      for (let classIdx in this.targets) {
        for (let imgIdx in this.targets[classIdx].images) {
          this.targets[classIdx].images[imgIdx].selected = false
        }
      }
    },

    gotoTop () {
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


#select-image
  img
    width: 18.5%
    margin: 2px

  .img-selectable
    border: 1px solid #000

  .img-selectable:hover
    border: 5px solid darken($turquoise, 10)

  .img-selected
    border: 5px solid $turquoise

#report-influence
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
