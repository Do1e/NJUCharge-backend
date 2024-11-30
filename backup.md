<style>
  select {
    padding: 5px;
    margin-left: 10px;
    border-radius: 5px;
    border: 1px solid #ced4da;
    font-size: 14px;
  }
  table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin-top: 10px !important;
  }
  table, th, td {
    border: 1px solid black !important;
    font-weight: bold !important;
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
  }
  .blue-text {
    color: #00A0FF;
  }
  .yellow-text {
    color: #FFB000;
  }
  .red-text {
    color: #FF7030;
  }
</style>

[点击此处查看新版UI](/charge.html)

:::warning
可用时间为预期可用时间，可能由于充满等原因提前结束
:::

<div class="filter-container"><label for="filter-station">选择站点:</label><select id="filter-station"><option value="">All</option><option value="05栋">05栋</option><option value="17栋">17栋</option><option value="18栋">18栋</option><option value="24栋">24栋</option><option value="26栋">26栋</option><option value="27栋">27栋</option><option value="天文学院">天文学院</option><option value="游泳馆">游泳馆</option><option value="第十餐厅">第十餐厅</option></select></div>

<table id="outletTable">
  <thead>
    <tr>
      <th>Station</th>
      <th>Name</th>
      <th>Rest Minutes</th>
      <th>Available Time</th>
      <th>Used Minutes</th>
      <th>Message</th>
      <th>Update Time</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>

后端代码和当前页面的前端代码开源在 [Do1e/NJUCharge-backend](https://github.com/Do1e/NJUCharge-backend)，欢迎提交issues  
前端（包括这一整个网站）基于 [Mix Space](https://github.com/mx-space) & [Shiro](https://github.com/innei/Shiro)。

[点击此处下载历史数据](https://alist.do1e.cn/%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6/%E5%8D%97%E5%A4%A7%E4%BB%99%E6%9E%97%E5%85%85%E7%94%B5%E6%A1%A9%E7%8A%B6%E6%80%81%E5%8E%86%E5%8F%B2%E6%95%B0%E6%8D%AE)


剩余时间restmin的3种颜色：
1. `restmin <= 20`：<span style="color: #00A0FF">0x00A0FF █</span>
2. `20 < restmin <= 120`：<span style="color: #FFB000">0xFFB000 █</span>
3. `restmin > 120`：<span style="color: #FF7030">0xFF7030 █</span>

<script>
// 获取表格中的数据并赋予颜色
function fetchData() {
  fetch('/files/outlets.json')
    .then(response => response.json())
    .then(data => {
      const tableBody = document.getElementById('outletTable').getElementsByTagName('tbody')[0];
      const rows = tableBody.getElementsByTagName('tr');
      while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
      }
      data.forEach(outlet => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = outlet.station;
        row.insertCell(1).textContent = outlet.name;
        row.insertCell(2).textContent = outlet.restmin;
        row.insertCell(3).textContent = outlet.available_time;
        row.insertCell(4).textContent = outlet.usedmin;
        row.insertCell(5).textContent = outlet.msg;
        row.insertCell(6).textContent = outlet.update_time;

        if (outlet.restmin <= 20) {
          row.cells[2].className = 'blue-text';
        } else if (outlet.restmin > 120) {
          row.cells[2].className = 'red-text';
        } else {
          row.cells[2].className = 'yellow-text';
        }

        if (outlet.msg === "空闲") {
          row.cells[5].className = 'blue-text';
        } else if (outlet.msg === "故障") {
          row.cells[5].className = 'red-text';
        } else {
          row.cells[5].className = 'yellow-text';
        }
      });
    })
    .catch(error => {
      console.error('Error fetching data: ', error);
    })
    .finally(() => {
      filterTable();
    });
}
fetchData();
</script>
<script>
// 筛选功能实现
var filter = document.getElementById('filter-station');
var urlParams = new URLSearchParams(window.location.search);
var initialFilter = urlParams.get('filter') || '';
filter.value = initialFilter;
filterTable();

filter.addEventListener('change', function() {
  var selectedValue = filter.value;
  if (selectedValue === '') {
    urlParams.delete('filter');
  } else {
    urlParams.set('filter', selectedValue);
  }
  if (urlParams.toString() === '') {
    window.history.replaceState({}, '', location.pathname);
  } else {
    window.history.replaceState({}, '', `${location.pathname}?${urlParams}`);
  }
  filterTable();
});

function filterTable() {
  var rows = document.getElementsByTagName('tr');
  for (var i = 1; i < rows.length; i++) {
    var row = rows[i];
    var name = row.children[0].textContent.toLowerCase();
    var nameFilter = filter.value.toLowerCase();
    if (name.indexOf(nameFilter) !== -1 || nameFilter === '') {
      row.style.display = 'table-row';
    } else {
      row.style.display = 'none';
    }
  }
}
</script>
