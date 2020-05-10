<template>
  <pre v-html="msg"></pre>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Stats',
  data () {
    return {
      msg: ''
    }
  },
  methods: {
    getMessage () {
      const path = '/info'
      axios.get(path)
        .then((res) => {
          this.msg = JSON.stringify(res.data, null, 2)
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    this.getMessage()
  }
}
</script>
