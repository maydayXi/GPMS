// 12 小時事件
function _12() {
  updatePast(AxisX12(), pm25_lst[site]['12'], site);
}

// 6 小時事件
function _6() {
  updatePast(AxisX6(), pm25_lst[site]['6'], site);
}

// 1 小時事件
function _1() {
  updatePast(AxisX1(), pm25_lst[site]['1'], site);
}
