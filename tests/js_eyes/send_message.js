// 获取输入框和按钮元素
const inputEl = document.querySelector('.n-input__textarea-el');
const submitBtn = document.querySelector('.n-button.n-button--primary-type.n-button--medium-type');

// 向输入框添加文本
inputEl.value = 'Hello, World!';
// 清空提示词
inputEl.setAttribute('placeholder', '');
// 等待1秒钟后模拟点击按钮
  // 删除按钮的禁用样式
submitBtn.classList.remove('n-button--disabled');
// 触发input事件
inputEl.dispatchEvent(new Event('input', { bubbles: true }));
setTimeout(function() {
  // 触发按钮点击事件
  submitBtn.click();
}, 100);