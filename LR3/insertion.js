function insertionSort(arr) {
  const len = arr.length;
  for (let i = 1; i < len; i++) {
    let j = i - 1;
    const tmp = arr[i];
    while (j >= 0 && arr[j] > tmp) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = tmp;
  }
  return arr;
}