<template>
<section class="section">
  <div class="container">
    <h1 class="title is-1">Demo for Upweighting influence function</h1>
    <p>This demo shows ... </p>
  </div>

  <div class="container content" id="select-network">
    <hr>
    <p class="subtitle is-3">1. Select Network</p>
    <ul>
      <li><a v-scroll-to="'#select-image'" @click="showcase_step=1">Resnet 110, CIFAR-10 dataset</a></li>
    </ul>
  </div>

  <div class="container" id="select-image">
    <div v-if="showcase_step>=1">
      <hr>
      <p class="subtitle is-3">2. Select test image</p>
      <tabs :only-fade="false" ref="tabs" type="boxed">
        <tab-pane v-for="aClass, classIdx in targets" :label="aClass.name" :key="classIdx">
          <a v-for="item, imgIdx in aClass.images" @click="showcase_step=2; onSelectTarget(aClass.name, imgIdx)" v-scroll-to="'#report-classification'">
            <img :src="item.src" :class="item.selected?'img-selected': ''" :key="imgIdx" class="img-selectable">
          </a>
        </tab-pane>
      </tabs>
    </div>
  </div>

  <div class="container" id="report-classification">
    <div v-show="showcase_step>=2">
      <hr>
      <p class="subtitle is-3">3. Classification result</p>
      <accuracy-chart :chartData="chartData" :width="400" :height="150"/>
      <br><br>
      <button class="button is-success" v-scroll-to="'#report-influence'" @click="showcase_step=3; onSelectHelpfulSample()">Helpful samples</button>
      <button class="button is-danger" v-scroll-to="'#report-influence'" @click="showcase_step=3; onSelectHarmfulSample()">Harmful samples</button>
    </div>
  </div>

  <div class="container" id="report-influence">
    <div class="content" v-show="showcase_step>=3">
      <hr>
      <p class="subtitle is-3">4. Upweighting Influence Result</p>
      <p class="subtitle is-4">{{ influence_info.title }}</p>
      <img v-for="item in influence_info.samples" :src="item">
    </div>
  </div>

  <div class="container" id="tail">
    <div v-show="showcase_step>=3">
      <br>
      <button class="button is-danger" v-scroll-to="'#select-network'" @click="showcase_step=0">Go to the first step</button>
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

  data () {
    return {
      classes: [
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
      ],
      targets: null,
      showcase_step: 0,
      influence_info: {
        title: '',
        samples: null
      },
      chartData: {
        labels: [
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
        ],
        datasets: [
          {
            label: 'test result',
            backgroundColor: 'rgba(255, 99, 132, 0.4)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 1,
            data: [0.01, 0.02, 0.03, 0.9, 0.01, 0.01, 0.1, 0.01, 0.01, 0.01]
          }
        ]
      },
      results_helpful: null,
      results_harmful: null,
      database: null
    }
  },

  mounted () {
    let self = this
    axios.get('/static/demo_database.json')
    .then(function (response) {
      self.database = response.data

      let targets = []
      for (let i in self.classes) {
        i = parseInt(i)
        let aClass = {name: self.classes[i], images: []}
        for (let j in _.range(5)) {
          j = parseInt(j)
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
      for (let classIdx in this.targets) {
        for (let imgIdx in this.targets[classIdx].images) {
          this.targets[classIdx].images[imgIdx].selected = false
        }
      }

      let classIdx
      for (let i in this.classes) {
        if (this.classes[i] === className) {
          classIdx = i
          break
        }
      }

      this.targets[classIdx].images[idx].selected = true

      let row = this.database[classIdx * 5 + idx]
      this.results_helpful = _.map(row['helpful'], (i) => '/static/train_images/' + i + '.png')
      this.results_harmful = _.map(row['harmful'], (i) => '/static/train_images/' + i + '.png')

      let chartData = _.clone(this.chartData)
      chartData.datasets[0].data = row.pred
      this.chartData = chartData
    },

    onSelectHelpfulSample () {
      this.influence_info.title = 'Helpful train samples: To decrease loss'
      this.influence_info.samples = this.results_helpful
    },

    onSelectHarmfulSample () {
      this.influence_info.title = 'Harmful train samples: To increase loss'
      this.influence_info.samples = this.results_harmful
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
    width: 19%

  .img-selectable
    border: 3px solid #ffff

  .img-selectable:hover
    border: 3px solid $primary

  .img-selected
    border: 3px solid $info

#report-influence img
  width: 19%
  border: 1px solid #000
  margin: 2px

</style>
