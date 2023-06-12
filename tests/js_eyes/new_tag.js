// 创建一个新的 script 标签
var script = document.createElement('script');

// 设置 script 标签的属性 src 和 type
script.src = 'path/to/your/script.js';
script.type = 'text/javascript';

// 将 script 标签添加到页面中
document.head.appendChild(script);
// 定义一个要执行的函数
function myFunction() {
  console.log('Hello, world!');
}

// 在控制台中调用该函数
eval('myFunction()');
