const targetNode = document.documentElement;
const config = { childList: true, subtree: true };

cur_content = "null";

const getTextContent = () => {
  // const elements = document.querySelectorAll('.overflow-hidden.text-sm.items-end, .overflow-hidden.text-sm.items-start');
  const elements = document.querySelectorAll('.overflow-hidden.text-sm.items-start');
  let content = '';
  // elements.forEach(element => {
  //   content += element.textContent;
  // });
  content = elements[elements.length-1].textContent;
  console.log(content);
  return content
};

// 初始获取一次内容
// getTextContent();

// 监听整个文档树的子节点变化
const observer = new MutationObserver(mutationsList => {
  for (let mutation of mutationsList) {
    if (mutation.type === 'childList') {  
      let timely_content = "";
      setTimeout(function() {
        timely_content = getTextContent();
        if(cur_content == timely_content)
        {
          console.log("应该是输出结束了");
        }
        cur_content = timely_content;
      }, 5000);
    }
  }
});

observer.observe(targetNode, config);