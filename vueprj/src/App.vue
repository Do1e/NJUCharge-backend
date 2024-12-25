<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const sortedStations = ref([])
const update_time = ref('')
const num_unoccupied = ref({})
const num_less20 = ref({})
const outlets = ref([])
const filtered_outlets = ref([])
const filter_name = ref('')
var urlParams = new URLSearchParams(window.location.search);
filter_name.value = urlParams.get('filter') || '';

async function fetchData() {
  const response = await fetch('/outlets.json');
  const data = await response.json();
  outlets.value = data;
  filterTable(filter_name.value);
  let stations = new Set();
  data.forEach(outlet => {
    stations.add(outlet.station)
  });
  sortedStations.value = Array.from(stations).sort();
  update_time.value = data[0].update_time.slice(0, -3);

  sortedStations.value.forEach(station => {
    num_unoccupied.value[station] = 0;
    num_less20.value[station] = 0;
  });
  data.forEach(outlet => {
    if (outlet.restmin === 0) {
      num_unoccupied.value[outlet.station]++;
    } else if (outlet.restmin <= 20) {
      num_less20.value[outlet.station]++;
    }
  });
}

function filterTable(filterName) {
  if (filterName === '') {
    filtered_outlets.value = outlets.value;
    urlParams.delete('filter');
  } else {
    filtered_outlets.value = [];
    outlets.value.forEach(outlet => {
      if (outlet.station === filterName) {
        filtered_outlets.value.push(outlet);
      }
    });
    urlParams.set('filter', filterName);
  }
  if (urlParams.toString() === '') {
    window.history.replaceState({}, '', location.pathname);
  } else {
    window.history.replaceState({}, '', `${location.pathname}?${urlParams}`);
  }
}

watch(filter_name, filterTable)

const outletClass = computed(() => {
  return outlet => {
    if (outlet.restmin === 0) {
      return 'unoccupied';
    } else if (outlet.restmin <= 20) {
      return 'restmin-1-20';
    } else if (outlet.restmin <= 120) {
      return 'restmin-21-120';
    } else if (outlet.restmin < 65535) {
      return 'restmin-121-unknow';
    } else if (outlet.restmin === 65535 && outlet.msg === '分钟计费模式') {
      return 'unkown';
    } else {
      return 'error';
    }
  };
});

const outletStatusClass = computed(() => {
  return outlet => {
    if (outlet.restmin === 0) {
      return 'outlet-status-unoccupied';
    } else if (outlet.restmin <= 20) {
      return 'outlet-status-restmin-1-20';
    } else if (outlet.restmin <= 120) {
      return 'outlet-status-restmin-21-120';
    } else if (outlet.restmin < 65535) {
      return 'outlet-status-restmin-121-unknow';
    } else if (outlet.restmin === 65535 && outlet.msg === '分钟计费模式') {
      return 'outlet-status-unkown';
    } else {
      return 'outlet-status-error';
    }
  };
});

const outletMsgClass = computed(() => {
  return outlet => {
    if (outlet.restmin === 0) {
      return 'outlet-msg-unoccupied';
    } else if (outlet.restmin < 65535) {
      return 'outlet-msg-known';
    } else if (outlet.restmin === 65535 && outlet.msg === '分钟计费模式') {
      return 'outlet-msg-unkown';
    } else {
      return 'outlet-msg-error';
    }
  };
});

onMounted(() => {
  fetchData();
})

</script>

<template>

  <table>
    <thead>
      <tr>
        <th><div>
          <label>选择站点:</label>
          <select v-model="filter_name">
            <option value="">All</option>
            <option v-for="station in sortedStations" :key="station" :value="station">{{ station }}</option>
          </select>
        </div></th>
        <th>空闲</th>
        <th>20分钟内</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="station in sortedStations" :key="station">
        <td>{{ station }}</td>
        <td :class="{ 'zero': num_unoccupied[station] === 0, 'notzero': num_unoccupied[station] > 0 }">{{ num_unoccupied[station] }}</td>
        <td :class="{ 'zero': num_less20[station] === 0, 'notzero': num_less20[station] > 0 }">{{ num_less20[station] }}</td>
      </tr>
    </tbody>
  </table>
  <div style="display: flex;">更新时间：{{ update_time }}</div>
  <div class="outletslist">
    <div v-for="outlet in filtered_outlets" class="outlet" :class="outletClass(outlet)">
      <div class="outlet-header">
        <div class="outlet-station">{{ outlet.station }}</div>
        <div class="outlet-name">{{ outlet.name }}</div>
      </div>
      <div class="outlet-status">
        <div class="outlet-status-unoccupied" v-if="outlet.restmin === 0">当前可用</div>
        <div :class="outletStatusClass(outlet)" v-else-if="outlet.restmin < 65535">
          <div class="outlet-status-restmin-detail">预计等待{{ outlet.restmin }}分钟</div>
          <div class="outlet-status-availabletime-detail">{{ outlet.available_time }}</div>
        </div>
        <div class="outlet-status-error" v-else-if="outlet.restmin === 65535 && outlet.msg === '分钟计费模式'">
          <div class="outlet-status-unkown">可用时间未知</div>
          <div class="outlet-status-usedmin">已使用{{ outlet.usedmin }}分钟</div>
        </div>
        <div class="outlet-msg-error" v-else>
          <div class="outlet-status-error">可用时间未知</div>
        </div>
      </div>
      <div class="outlet-msg">
        <div :class="outletMsgClass(outlet)">{{ outlet.msg }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
select {
  padding: 5px;
  margin-left: 10px;
  border-radius: 5px;
  border: 1px solid #ced4da;
  font-size: 14px;
}
.outletslist {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  box-sizing: border-box;
}
.outlet {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  flex-direction: column;
  justify-content: space-between;
  width: calc(25% - 48px);
  box-sizing: border-box;
  flex-grow: 1;
}
@media (max-width: 1000px) {
  .outlet {
    width: calc(33.33333% - 32px);
  }
}
@media (max-width: 600px) {
  .outlet {
    width: calc(50% - 16px);
  }
}
@media (max-width: 400px) {
  .outlet {
    width: 100%;
  }
}
.outlet.unoccupied {
  background-color: #7cff9b40;
}
.outlet.restmin-1-20 {
  background-color: #7fceff40;
}
.outlet.restmin-21-120 {
  background-color: #ffdc7a40;
}
.outlet-header {
  display: flex;
  align-items: center;
  font-weight: bold;
  justify-content: flex-start;
  gap: 8px;
}
.outlet-updatetime {
  display: flex;
  gap: 4px;
  align-items: center;
  font-size: 12px;
  color: #888;
}
.outlet-status {
  flex-wrap: wrap;
  align-items: center;
  font-size: 14px;
}
.outlet-status-unoccupied {
  color: #00A0FF;
  font-weight: bold;
}
.outlet-status-restmin-1-20 {
  color: #00A0FF;
}
.outlet-status-restmin-21-120 {
  color: #FFB000;
}
.outlet-status-restmin-121-unknow, .outlet-status-error, .outlet-status-unkown {
  color: #FF7030;
}
.outlet-msg-error {
  color: #FF0000;
}
.outlet-msg {
  color: #666;
  font-size: 14px;
}
.outlet-updatetime {
  color: #888;
  font-size: 12px;
}
table {
  width: 100% !important;
  border-collapse: collapse !important;
  margin-top: 10px !important;
}
table, th, td {
  border: 1px solid #555 !important;
}
th, td {
  padding: 8px !important;
  text-align: left !important;
}
thead {
  background-color: rgba(255, 255, 255, 0) !important;
}
tr {
  background-color: rgba(255, 255, 255, 0) !important;
}
th {
  position: sticky !important;
  top: 0 !important;
  width: calc(100% / 3) !important;
}
td.zero {
  color: #808080;
}
td.notzero {
  color: #00A0FF;
  font-weight: 'bold';
}
</style>
